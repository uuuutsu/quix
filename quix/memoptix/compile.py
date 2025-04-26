from collections.abc import Iterable
from logging import warning
from typing import Literal, overload

from quix.core.opcodes import CoreOpcode, CoreOpcodes, CoreProgram, Ref
from quix.memoptix.scheduler import (
    Array,
    BaseConstraint,
    Blueprint,
    HardLink,
    Index,
    LifeCycle,
    Owner,
    Scheduler,
    SoftLink,
    create_resolver_registry,
    create_slider_registry,
)

from .opcodes import MemoptixOpcodes
from .utils import find_optimal_usage_scope


def compile(program: CoreProgram) -> tuple[CoreProgram, dict[Ref, int]]:
    scopes = get_ref_scopes(program)
    owners = create_owners(list(scopes.keys()))

    blueprints = create_blueprints_by_domain(create_constraints(program, owners, scopes))
    layout = Scheduler(create_resolver_registry(), create_slider_registry()).schedule(*blueprints)

    memory = {owner.ref: index for owner, index in layout.mapping().items()}

    return strip_program(program), memory


@overload
def get_ref_scopes(program: CoreProgram, *, close: Literal[True] = True) -> dict[Ref, tuple[int, int]]: ...
@overload
def get_ref_scopes(program: CoreProgram, *, close: Literal[False] = False) -> dict[Ref, tuple[int, int | None]]: ...
def get_ref_scopes(
    program: CoreProgram, *, close: bool = True
) -> dict[Ref, tuple[int, int | None]] | dict[Ref, tuple[int, int]]:
    rough_usages: dict[Ref, tuple[int, int | None]] = {}
    loops: list[tuple[int, int]] = []
    curr_opcode_idx: int = 0
    for opcode in program:
        if (ref := opcode.args().get("ref")) is None:
            ...
        elif opcode.__id__ == CoreOpcodes.LOOP:
            loop_program = opcode.args()["program"]
            internal_rough_usages = get_ref_scopes(loop_program, close=False)

            adjusted_idx = curr_opcode_idx + 1
            for ref, (start, end) in internal_rough_usages.items():
                if ref not in rough_usages:
                    adjusted_end = None if end is None else adjusted_idx + end
                    rough_usages[ref] = adjusted_idx + start, adjusted_end
                else:
                    if rough_usages[ref][-1] is not None:
                        warning(f"Using freed reference. Freeing discarded: {ref}")

                    adjusted_end = None if end is None else adjusted_idx + end
                    rough_usages[ref] = rough_usages[ref][0], adjusted_end

            loop_ref = opcode.args()["ref"]
            if (loop_ref in rough_usages) and (rough_usages[loop_ref][-1] is not None):
                warning(f"Loop's owning ref is freed inside the loop. Freeing discared: {loop_ref}")
                rough_usages[loop_ref] = rough_usages[loop_ref][0], None
            elif loop_ref not in rough_usages:
                rough_usages[loop_ref] = curr_opcode_idx, None

            loops.append((curr_opcode_idx, curr_opcode_idx + len(loop_program)))
            curr_opcode_idx += len(loop_program)
            continue

        elif opcode.__id__ == MemoptixOpcodes.FREE:
            if ref not in rough_usages:
                warning(f"Freeing unused reference: {ref}")
                rough_usages[ref] = (curr_opcode_idx, None)
            elif rough_usages[ref][1] is not None:
                warning(f"Refreeing reference: {ref}")

            rough_usages[ref] = rough_usages[ref][0], curr_opcode_idx

        elif (ref in rough_usages) and (rough_usages[ref][-1] is not None):
            warning(f"Using freed reference. Freeing discarded: {ref}")
            rough_usages[ref] = rough_usages[ref][0], None
        elif ref not in rough_usages:
            rough_usages[ref] = curr_opcode_idx, None

        curr_opcode_idx += 1

    if not close:
        return rough_usages

    adjusted_usages: dict[Ref, tuple[int, int]] = {}
    for ref, (start_, end_) in rough_usages.items():
        end_ = end_ if end_ is not None else curr_opcode_idx
        adjusted_usages[ref] = find_optimal_usage_scope((start_, end_), loops)

    return adjusted_usages


def create_owners(refs: Iterable[Ref]) -> dict[Ref, Owner]:
    mapping: dict[Ref, Owner] = {}

    for ref in refs:
        mapping[ref] = Owner(None, ref=ref)

    return mapping


def create_constraints(
    program: CoreProgram,
    mapping: dict[Ref, Owner],
    lifecycles: dict[Ref, tuple[int, int]],
) -> dict[Owner, list[BaseConstraint]]:
    constrs: dict[Owner, list[BaseConstraint]] = {}

    for opcode in program:
        args = opcode.args()
        own_constrs = constrs.setdefault(mapping[args.pop("ref")], [])
        match opcode.__id__:
            case MemoptixOpcodes.INDEX:
                own_constrs.append(Index(**args))
            case MemoptixOpcodes.ARRAY:
                own_constrs.append(Array(**args))
            case MemoptixOpcodes.HARD_LINK:
                hard_to_ = mapping[args.pop("to_")]
                own_constrs.append(HardLink(hard_to_, **args))
            case MemoptixOpcodes.SOFT_LINK:
                soft_to_: dict[Owner, int] = {mapping[ref]: scale for ref, scale in args["to_"]}
                own_constrs.append(SoftLink(soft_to_))

    for ref, cycle in lifecycles.items():
        own_constrs = constrs.setdefault(mapping[ref], [])
        own_constrs.append(LifeCycle(*cycle))

    return constrs


def create_blueprints_by_domain(constraints: dict[Owner, list[BaseConstraint]]) -> list[Blueprint]:
    domain2constr: dict[tuple[type[BaseConstraint], ...], dict[Owner, list[BaseConstraint]]] = {}

    for owner, constrs in constraints.items():
        domain = tuple(type(constr) for constr in constrs)
        domain2constr.setdefault(domain, {})[owner] = constrs

    blueprints: list[Blueprint] = []
    for constr_set in domain2constr.values():
        new_blueprint = Blueprint()
        for owner, constrs in constr_set.items():
            new_blueprint.add_constraints(owner, *constrs)

        blueprints.append(new_blueprint)

    return blueprints


def strip_program(program: CoreProgram) -> CoreProgram:
    new_program: list[CoreOpcode] = []
    for opcode in program:
        if opcode.__id__ in MemoptixOpcodes:
            continue
        new_program.append(opcode)
    return new_program

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


def mem_compile(program: CoreProgram, garbage_collector: bool = True) -> tuple[CoreProgram, dict[Ref, int]]:
    scopes = get_ref_scopes(program, garbage_collector)
    owners = create_owners(list(scopes.keys()))

    constrs = create_constraints(program, owners)
    cycle_constrs = create_lifecycle_constraints(owners, scopes)
    constraints = merge_constraints(constrs, cycle_constrs)

    blueprints = create_blueprints(constraints)
    layout = Scheduler(create_resolver_registry(), create_slider_registry()).schedule(*blueprints)

    memory = {owner.ref: index for owner, index in layout.mapping().items()}

    return strip_program(program), memory


@overload
def get_ref_scopes(
    program: CoreProgram,
    garbage_collector: bool = True,
    *,
    close: Literal[True] = True,
) -> dict[
    Ref,
    tuple[int, int],
]: ...
@overload
def get_ref_scopes(
    program: CoreProgram,
    garbage_collector: bool = True,
    *,
    close: Literal[False] = False,
) -> tuple[
    dict[Ref, tuple[int, int | None]],
    list[tuple[int, int]],
    int,
]: ...
def get_ref_scopes(
    program: CoreProgram,
    garbage_collector: bool = True,
    *,
    close: bool = True,
) -> (
    tuple[
        dict[Ref, tuple[int, int | None]],
        list[tuple[int, int]],
        int,
    ]
    | dict[
        Ref,
        tuple[int, int],
    ]
):
    rough_usages: dict[Ref, tuple[int, int | None]] = {}
    loops: list[tuple[int, int]] = []
    stack: list[tuple[Ref, int]] = []
    curr_opcode_idx: int = 0
    length: int = 0

    for opcode in program:
        if opcode.__id__ == CoreOpcodes.END_LOOP:
            ref, idx = stack.pop()
            loops.append((idx, curr_opcode_idx))
        elif (ref := opcode.args().get("ref")) is None:
            ...

        if opcode.__id__ == CoreOpcodes.START_LOOP:
            stack.append((ref, curr_opcode_idx))

        if opcode.__id__ == MemoptixOpcodes.FREE:
            if ref not in rough_usages:
                if close is True:
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
        length += 1

    if not close:
        return rough_usages, loops, length

    adjusted_usages: dict[Ref, tuple[int, int]] = {}
    for ref, (start_, end_) in rough_usages.items():
        if garbage_collector is False:
            adjusted_usages[ref] = (0, curr_opcode_idx - 1)
            continue
        end_ = end_ if end_ is not None else curr_opcode_idx - 1
        adjusted_usages[ref] = find_optimal_usage_scope((start_, end_), loops)

    return adjusted_usages


def create_owners(refs: Iterable[Ref]) -> dict[Ref, Owner]:
    mapping: dict[Ref, Owner] = {}

    for ref in refs:
        mapping[ref] = Owner(None, ref=ref)

    return mapping


def merge_constraints(
    left: dict[Owner, list[BaseConstraint]], right: dict[Owner, list[BaseConstraint]]
) -> dict[Owner, list[BaseConstraint]]:
    constrs: dict[Owner, list[BaseConstraint]] = left
    for owner, right_constrs in right.items():
        if owner in constrs:
            constrs[owner].extend(right_constrs)
        else:
            constrs[owner] = right_constrs
    return constrs


def create_lifecycle_constraints(
    mapping: dict[Ref, Owner],
    lifecycles: dict[Ref, tuple[int, int]],
) -> dict[Owner, list[BaseConstraint]]:
    constrs: dict[Owner, list[BaseConstraint]] = {}
    for ref, cycle in lifecycles.items():
        own_constrs = constrs.setdefault(mapping[ref], [])
        own_constrs.append(LifeCycle(*cycle))
    return constrs


def create_constraints(
    program: CoreProgram,
    mapping: dict[Ref, Owner],
) -> dict[Owner, list[BaseConstraint]]:
    constrs: dict[Owner, list[BaseConstraint]] = {}

    for opcode in program:
        args = opcode.args()

        if (ref := args.pop("ref", None)) is None:
            continue

        own_constrs = constrs.setdefault(mapping[ref], [])
        match opcode.__id__:
            case MemoptixOpcodes.INDEX:
                own_constrs.append(Index(**args))
            case MemoptixOpcodes.ARRAY:
                own_constrs.append(Array(**args))
            case MemoptixOpcodes.HARD_LINK:
                hard_to_ = mapping[args.pop("to_")]
                own_constrs.append(HardLink(hard_to_, **args))
            case MemoptixOpcodes.SOFT_LINK:
                soft_to_: dict[Owner, int] = {mapping[ref]: scale for ref, scale in args["to_"].items()}
                own_constrs.append(SoftLink(soft_to_))

    return constrs


def create_blueprints(constraints: dict[Owner, list[BaseConstraint]]) -> list[Blueprint]:
    domain2constr: list[
        dict[
            tuple[type[BaseConstraint], ...],
            dict[Owner, list[BaseConstraint]],
        ]
    ] = []

    for constr_set in group_constraints_by_owners(constraints):
        constr_mapping: dict[
            tuple[type[BaseConstraint], ...],
            dict[Owner, list[BaseConstraint]],
        ] = {}
        for owner, constrs in constr_set.items():
            domain = tuple(type(constr) for constr in constrs)
            constr_mapping.setdefault(domain, {})[owner] = constrs
        domain2constr.append(constr_mapping)

    blueprints: list[Blueprint] = []
    array_bps: list[Blueprint] = []
    for constr_mapping in domain2constr:
        new_blueprint = Blueprint()
        is_array: bool = False
        for domain, constr_set in constr_mapping.items():
            for owner, constrs in constr_set.items():
                new_blueprint.add_constraints(owner, *constrs)

            is_array = Array in domain

        (array_bps if is_array else blueprints).append(new_blueprint)

    return blueprints + array_bps


def group_constraints_by_owners(
    constraints: dict[Owner, list[BaseConstraint]],
) -> list[dict[Owner, list[BaseConstraint]]]:
    owner2mapping: dict[Owner, dict[Owner, list[BaseConstraint]]] = {}
    roots: list[Owner] = []

    for owner, constrs in constraints.items():
        if owner not in owner2mapping:
            owner2mapping[owner] = {}
            roots.append(owner)

        mapping = owner2mapping[owner]
        mapping[owner] = constrs

        for constr in constrs:
            for related_owner in constr.get_owners():
                owner2mapping[related_owner] = mapping

    unique_list = [owner2mapping[owner] for owner in roots]
    return unique_list


def strip_program(program: CoreProgram) -> CoreProgram:
    new_program: list[CoreOpcode] = []
    for opcode in program:
        if opcode.__id__ in MemoptixOpcodes:
            continue
        new_program.append(opcode)
    return new_program

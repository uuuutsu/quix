from collections.abc import Iterable
from logging import warning
from typing import Literal, overload

from quix.core.opcodes.dtypes import CoreProgram, Ref
from quix.memoptix.opcodes import MemoptixOpcodes
from quix.memoptix.scheduler.tree import Array, HardLink, Index, Node, SoftLink, create_node

from .utils import find_optimal_usage_scope

type RefScopes = dict[Ref, tuple[int, int]]


def program_to_trees(program: CoreProgram, garbage_collector: bool = True) -> list[Node]:
    scopes = get_ref_scopes(program, garbage_collector)
    nodes = create_nodes(program, scopes)
    roots = get_roots(nodes)
    return roots


@overload
def get_ref_scopes(
    program: CoreProgram,
    garbage_collector: bool = True,
    *,
    close: Literal[True] = True,
) -> RefScopes: ...
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
        if opcode.__id__ == "end_loop":
            ref, idx = stack.pop()
            loops.append((idx, curr_opcode_idx))
        elif (ref := opcode.args().get("ref")) is None:
            ...

        elif opcode.__id__ == MemoptixOpcodes.FREE:
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

        if opcode.__id__ == "start_loop":
            stack.append((ref, curr_opcode_idx))

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


def create_nodes(program: CoreProgram, scopes: RefScopes) -> Iterable[Node]:
    mapping: dict[Ref, Node] = {}

    def _get_scope(ref: Ref, parent: Ref) -> tuple[int, int]:
        # TODO: Handle hidden reference's scopes correctly. Either here or in `get_ref_scopes`
        return scopes.get(ref, scopes[parent])

    def _get_node(ref: Ref, parent: Ref) -> Node:
        if ref not in mapping:
            mapping[ref] = create_node(_get_scope(ref, parent), ref=ref, name=None)
        return mapping[ref]

    for opcode in program:
        args = opcode.args()

        if (ref := args.pop("ref", None)) is None:
            continue

        match opcode.__id__:
            case MemoptixOpcodes.INDEX:
                _get_node(ref, ref).add_constraint(Index(**args))

            case MemoptixOpcodes.ARRAY:
                _get_node(ref, ref).add_constraint(Array(**args))

            case MemoptixOpcodes.HARD_LINK:
                to_ = args.pop("to_")
                _get_node(ref, ref).add_constraint(HardLink(_get_node(to_, ref), **args))

            case MemoptixOpcodes.SOFT_LINK:
                to_refs: dict[Ref, int] = args.pop("to_")
                to_nodes: dict[Node, int] = {}
                for to_ref, scale in to_refs.items():
                    to_nodes[_get_node(to_ref, ref)] = scale
                _get_node(ref, ref).add_constraint(SoftLink(to_=to_nodes))

            case _:
                _get_node(ref, ref)

    return mapping.values()


def get_roots(nodes: Iterable[Node]) -> list[Node]:
    seen: set[Node] = set()
    roots: list[Node] = []

    for node in _flatten_nodes(*nodes):
        seen.add(node)

    for node in nodes:
        if node not in seen:
            roots.append(node)

    return roots


def _flatten_nodes(*nodes: Node, add_root: bool = False) -> set[Node]:
    if not nodes:
        return set()

    seen: set[Node] = set()
    for node in nodes:
        for constr in node.constraints:
            seen.update(_flatten_nodes(*constr.get_nodes(), add_root=True))
        if add_root:
            seen.add(node)
    return seen

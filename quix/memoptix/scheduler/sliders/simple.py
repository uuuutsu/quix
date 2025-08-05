from quix.memoptix.scheduler.layout import Layout
from quix.memoptix.scheduler.tree import (
    Array,
    HardLink,
    Index,
    Node,
    SoftLink,
    flatten_node,
    get_constraint_groups,
)
from quix.tools import intervals_intersects

from .base import Slider


def _get_intersected_nodes_between_sets(left_nodes: list[Node], right_nodes: list[Node]) -> list[tuple[Node, Node]]:
    inter_pairs = []
    for node_left in left_nodes:
        for node_right in right_nodes:
            if not intervals_intersects(node_left.lifecycle, node_right.lifecycle):
                continue

            inter_pairs.append((node_left, node_right))
    return inter_pairs


def _simplify_array_constrs(arrays: dict[Node, list[Array]]) -> dict[Node, int]:
    new_arrays: dict[Node, int] = {}
    for node, (constr, *_) in arrays.items():
        if len(_) > 0:
            raise ValueError(f"At most one `{Array}` constraint is allowed for each node.")
        new_arrays[node] = constr.length
    return new_arrays


def _mappings_intersect(
    left: dict[Node, int],
    right: dict[Node, int],
    inter_pairs: list[tuple[Node, Node]],
    left_arrays: dict[Node, int],
    right_arrays: dict[Node, int],
) -> int:
    for left_node, right_node in inter_pairs:
        left_index = left[left_node]
        right_index = right[right_node]

        if intervals_intersects(
            (left_index, left_index + left_arrays.get(left_node, 1)),
            (right_index, right_index + right_arrays.get(right_node, 1)),
        ):
            return left_index + left_arrays.get(left_node, 1) - right_index

    return 0


def _slide_mapping(mapping: dict[Node, int], offset: int) -> dict[Node, int]:
    return {node: index + offset for node, index in mapping.items()}


class SimpleSlider(Slider):
    __slots__ = ()

    __domain__ = {Index, SoftLink, HardLink, Array}

    def __call__(self, left: Layout, right: Layout) -> Layout:
        left_nodes = list(flatten_node(*left.roots).keys())
        right_nodes = list(flatten_node(*right.roots).keys())
        if set(left_nodes).intersection(set(right_nodes)):
            raise RuntimeError("Trees can't reference same node.")

        left_constrs = get_constraint_groups(*left.roots)
        right_constrs = get_constraint_groups(*right.roots)
        if not left_constrs.get(Index, {}):
            left_constrs, right_constrs = right_constrs, left_constrs
            left, right = right, left
            left_nodes, right_nodes = right_nodes, left_nodes
        elif (not right_constrs.get(Array, {})) and left_constrs.get(Array, {}):
            left_constrs, right_constrs = right_constrs, left_constrs
            left, right = right, left
            left_nodes, right_nodes = right_nodes, left_nodes

        left_arrays = _simplify_array_constrs(left_constrs.get(Array, {}))  # type: ignore
        right_arrays = _simplify_array_constrs(right_constrs.get(Array, {}))  # type: ignore
        pos_inters = _get_intersected_nodes_between_sets(left_nodes, right_nodes)

        root_mapping = left.mapping()
        sliding_mapping = right.mapping()
        if right_constrs.get(Index, {}) and left_constrs.get(Index, {}):
            if _mappings_intersect(root_mapping, sliding_mapping, pos_inters, left_arrays, right_arrays) != 0:
                raise RuntimeError(
                    f"Layouts {left} and {right} cannot be combined due to coliding lifecycles on enforced indexes."
                )
            return Layout(root_mapping | sliding_mapping, left.roots + right.roots)

        offset: int = 0
        while True:
            sliding_mapping = _slide_mapping(sliding_mapping, offset)
            new_offset = _mappings_intersect(root_mapping, sliding_mapping, pos_inters, left_arrays, right_arrays)
            if new_offset != 0:
                offset += new_offset
                continue
            return Layout(root_mapping | sliding_mapping, left.roots + right.roots)

from quix.memoptix.scheduler.tree import Node
from quix.memoptix.scheduler.tree.constraints import Array, Index
from quix.memoptix.scheduler.tree.flatten import flatten_node


def extract_constraint_info(
    root: Node,
) -> tuple[
    dict[Node, int],
    dict[Node, int],
]:
    indexes: dict[Node, int] = {}
    arrays: dict[Node, int] = {}

    for node, constrs in flatten_node(root).items():
        for constr in constrs:
            match constr:
                case Index():
                    indexes[node] = constr.index
                case Array():
                    arrays[node] = constr.length
                case _:
                    raise RuntimeError(f"Unknown constraint: {constr}")

    return indexes, arrays


def order_ascend_with_array_in_the_back(arrays: dict[Node, int]) -> list[Node]:
    ordered: list[Node] = []
    array_nodes: dict[Node, int] = {}

    for pair in sorted(arrays.items(), key=lambda p: p[0].lifecycle[0]):
        node = pair[0]
        if node not in arrays:
            ordered.append(node)
        else:
            array_nodes[node] = arrays[node]

    for node, _ in sorted(array_nodes.items(), key=lambda p: p[1]):
        ordered.append(node)

    return ordered


def get_all_affected_nodes(node: Node, mapping: dict[Node, int], anchor: int, arrays: dict[Node, int]) -> set[Node]:
    nodes: set[Node] = set()

    for idx in range(
        anchor,
        anchor + arrays.get(node, 0) + 1,
    ):
        for existing_node, existing_idx in mapping.items():
            left, right = existing_idx, existing_idx + arrays.get(existing_node, 1)
            if left <= idx < right:
                nodes.add(existing_node)

    return nodes

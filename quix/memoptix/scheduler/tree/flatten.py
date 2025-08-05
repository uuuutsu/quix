from quix.memoptix.scheduler.tree.constraints.base import BaseConstraint
from quix.memoptix.scheduler.tree.node import Node


def flatten_node(*roots: Node) -> dict[Node, list[BaseConstraint]]:
    nodes: dict[Node, list[BaseConstraint]] = {}

    if not roots:
        return {}

    for root in roots:
        for costr in root.constraints:
            for child, contrs in flatten_node(*costr.get_nodes()).items():
                nodes.setdefault(child, []).extend(contrs)
        nodes.setdefault(root, []).extend(root.constraints)

    return nodes

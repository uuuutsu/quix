from quix.memoptixv2.scheduler.tree.constraints.base import BaseConstraint
from quix.memoptixv2.scheduler.tree.node import Node


def flatten_node(*roots: Node) -> dict[Node, list[BaseConstraint]]:
    nodes: dict[Node, list[BaseConstraint]] = {}
    for root in roots:
        for costr in root.constraints:
            for child in costr.get_nodes():
                nodes.update(flatten_node(child))
        nodes.setdefault(root, []).extend(root.constraints)
    return nodes

from quix.memoptix.scheduler.tree.constraints import BaseConstraint, HardLink, SoftLink
from quix.memoptix.scheduler.tree.flatten import flatten_node
from quix.memoptix.scheduler.tree.node import Node


def get_longest(*roots: Node) -> int:
    return max(len(flatten_node(root)) for root in roots)


def copy_node(node: Node) -> Node:
    new_node = Node(node.lifecycle, node.name, ref=node.ref, constraints=[])
    if not node.constraints:
        return new_node

    for constr in node.constraints:
        new_constr: BaseConstraint
        match constr:
            case HardLink():
                new_constr = HardLink(copy_node(constr.to_), constr.distance)
            case SoftLink():
                to_ = {}
                for node, scale in constr.to_.items():
                    to_[copy_node(node)] = scale
                new_constr = SoftLink(to_)
            case _:
                new_constr = type(constr)(**constr.__store__())  # type: ignore

        new_node.add_constraint(new_constr)

    return new_node

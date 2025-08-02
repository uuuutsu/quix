from quix.memoptixv2.scheduler.tree.constraints import BaseConstraint
from quix.memoptixv2.scheduler.tree.flatten import flatten_node
from quix.memoptixv2.scheduler.tree.node import Node

type Domain = set[type[BaseConstraint]]
type ConstraintMapper = dict[type[BaseConstraint], dict[Node, list[BaseConstraint]]]


def get_domain(*nodes: Node) -> set[type[BaseConstraint]]:
    constraint_types = set()
    for constrs in flatten_node(*nodes).values():
        for constr in constrs:
            constraint_types.add(type(constr))
    return constraint_types


def get_constraint_groups(root: Node) -> ConstraintMapper:
    mappers: ConstraintMapper = {}

    for node, constrs in flatten_node(root).items():
        for constr in constrs:
            mappers.setdefault(type(constr), {}).setdefault(node, []).append(constr)
    return mappers

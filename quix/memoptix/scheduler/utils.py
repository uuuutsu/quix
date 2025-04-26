from quix.memoptix.scheduler.blueprint import Blueprint
from quix.memoptix.scheduler.constraints import BaseConstraint
from quix.memoptix.scheduler.owner import Owner

type ConstraintMapper = dict[type[BaseConstraint], dict[Owner, list[BaseConstraint]]]


def get_constraint_mappers(blueprint: Blueprint) -> ConstraintMapper:
    mappers: ConstraintMapper = {}

    for owner, constr in blueprint.iter_constr():
        mappers.setdefault(type(constr), {}).setdefault(owner, []).append(constr)
    return mappers

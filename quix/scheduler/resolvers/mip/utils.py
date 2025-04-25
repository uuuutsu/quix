from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import BaseConstraint
from quix.scheduler.owner import Owner

type ConstraintMapper = dict[type[BaseConstraint], dict[Owner, list[BaseConstraint]]]


def get_constraint_mappers(blueprint: Blueprint) -> ConstraintMapper:
    mappers: ConstraintMapper = {}

    for owner, constr in blueprint.iter_constr():
        mappers.setdefault(type(constr), {}).setdefault(owner, []).append(constr)
    return mappers

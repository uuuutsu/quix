from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import BaseConstraint
from quix.scheduler.owner import Owner

type ConstraintMapper = dict[type[BaseConstraint], dict[Owner, list[BaseConstraint]]]


def get_constraint_mappers(blueprint: Blueprint) -> ConstraintMapper:
    mappers: ConstraintMapper = {}

    for owner, constr in blueprint.iter_constr():
        mappers.setdefault(type(constr), {}).setdefault(owner, []).append(constr)
    return mappers


def intervals_intersects(int1: tuple[int, int], int2: tuple[int, int]) -> bool:
    return max(int1[1], int2[1]) - min(int1[0], int2[0]) < (int1[1] - int1[0]) + (int2[1] - int2[0]) or (
        (int1[0] <= int2[0]) and (int1[1] >= int2[1])
    )

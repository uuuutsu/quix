import math
from collections.abc import Callable

from quix.memoptix.scheduler.blueprint import Blueprint
from quix.memoptix.scheduler.constraints import BaseConstraint
from quix.memoptix.scheduler.owner import Owner

type ConstraintMapper = dict[type[BaseConstraint], dict[Owner, list[BaseConstraint]]]
type Domain = set[type[BaseConstraint]]
type Matcher = Callable[[Domain, list[Domain]], int | None]


def get_constraint_mappers(blueprint: Blueprint) -> ConstraintMapper:
    mappers: ConstraintMapper = {}

    for owner, constr in blueprint.iter_constr():
        mappers.setdefault(type(constr), {}).setdefault(owner, []).append(constr)
    return mappers


def inclusion_matcher(to_match: Domain, registry: list[Domain]) -> int | None:
    curr_match: int | None = None
    curr_length: float = math.inf

    for idx, domain in enumerate(registry):
        if to_match - domain:
            continue
        if len(domain) < curr_length:
            curr_length = len(domain)
            curr_match = idx

    if curr_match is not None:
        return curr_match

    return None

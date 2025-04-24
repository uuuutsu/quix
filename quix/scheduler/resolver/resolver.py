from quix.scheduler.blueprint import Blueprint
from quix.scheduler.owner import Owner

from .utils import isolate_related_groups


class Resolver:
    __slots__ = ()

    def resolve(self, blueprints: list[Blueprint]) -> list[set[Owner]]:
        isolated_sets = isolate_related_groups(blueprints)
        return isolated_sets

from collections.abc import Callable

from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import BaseConstraint

from .group import Group
from .utils import isolate_related_groups

type Handler = Callable[[list[Blueprint]], Group]


class Resolver:
    __slots__ = "_tile_handlers"

    def __init__(self) -> None:
        self._tile_handlers: dict[tuple[type[BaseConstraint], ...], Handler] = {}

    def resolve(self, blueprints: list[Blueprint]) -> list[Group]:
        related_bps = isolate_related_groups(blueprints)
        groups: list[Group] = []

        for bps in related_bps:
            signature = {type for bp in bps for type in bp.get_constraint_types()}
            for key, handler in self._tile_handlers.items():
                if set(key) == signature:
                    groups.append(handler(list(bps)))
                    break
            else:
                raise RuntimeError(f"No handler found for contraint set: {signature}")
        return groups

    def add_handler(self, constraints: tuple[type[BaseConstraint], ...], handler: Handler) -> None:
        self._tile_handlers[constraints] = handler


def create_resolver() -> Resolver:
    resolver = Resolver()
    return resolver

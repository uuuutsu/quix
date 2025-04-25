from functools import cached_property

from rich.pretty import pretty_repr

from quix.scheduler.blueprint import Blueprint

from .owner import Owner


class Layout:
    __slots__ = (
        "_mapping",
        "blueprint",
    )

    def __init__(self, blueprint: Blueprint, mapping: dict[Owner, int]) -> None:
        self.blueprint = blueprint
        self._mapping: dict[Owner, int] = mapping

    def mapping(self) -> dict[Owner, int]:
        return self._mapping

    @cached_property
    def footprint(self) -> int:
        values = self._mapping.values()
        return max(values) - min(values) + 1

    def __repr__(self) -> str:
        return pretty_repr(self._mapping)

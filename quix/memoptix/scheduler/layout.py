from rich.pretty import pretty_repr

from quix.memoptix.scheduler.blueprint import Blueprint

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

    def __repr__(self) -> str:
        return pretty_repr(self._mapping)

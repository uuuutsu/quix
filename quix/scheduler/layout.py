from rich.pretty import pretty_repr

from quix.scheduler.blueprint import Blueprint

from .owner import Owner


class Layout:
    __slots__ = (
        "_mapping",
        "_blueprint",
        "absolute",
    )

    def __init__(self, blueprint: Blueprint, mapping: dict[Owner, int], absolute: bool = False) -> None:
        self._blueprint = blueprint
        self._mapping: dict[Owner, int] = mapping
        self.absolute = absolute

    def mapping(self) -> dict[Owner, int]:
        return self._mapping

    def __repr__(self) -> str:
        return pretty_repr(self._mapping)

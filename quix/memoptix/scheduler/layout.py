from __future__ import annotations

from rich.pretty import pretty_repr

from quix.memoptix.scheduler.tree import Node


class Layout:
    __slots__ = (
        "_mapping",
        "roots",
    )

    def __init__(self, mapping: dict[Node, int], roots: list[Node]) -> None:
        self.roots = roots
        self._mapping: dict[Node, int] = mapping

    def mapping(self) -> dict[Node, int]:
        return self._mapping

    def __repr__(self) -> str:
        return pretty_repr(self._mapping)

from __future__ import annotations

from rich.pretty import pretty_repr

from quix.memoptixv2.scheduler.tree import Node


class Layout:
    __slots__ = (
        "_mapping",
        "node",
    )

    def __init__(self, mapping: dict[Node, int], node: Node) -> None:
        self.node = node
        self._mapping: dict[Node, int] = mapping

    def mapping(self) -> dict[Node, int]:
        return self._mapping

    def __repr__(self) -> str:
        return pretty_repr(self._mapping)

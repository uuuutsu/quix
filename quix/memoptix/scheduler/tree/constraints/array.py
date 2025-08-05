from dataclasses import dataclass

from quix.memoptix.scheduler.tree.node import Node

from .base import BaseConstraint


@dataclass(slots=True, frozen=True)
class Array(BaseConstraint):
    length: int

    def get_nodes(self) -> set[Node]:
        return set()

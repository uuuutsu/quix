from dataclasses import dataclass
from typing import override

from quix.memoptix.scheduler.tree.node import Node

from .base import BaseConstraint


@dataclass(slots=True, frozen=True)
class SoftLink(BaseConstraint):
    to_: dict[Node, int]

    @override
    def get_nodes(self) -> set[Node]:
        return set(self.to_.keys())

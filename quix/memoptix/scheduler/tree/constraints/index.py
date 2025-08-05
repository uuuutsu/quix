from dataclasses import dataclass
from typing import override

from quix.memoptix.scheduler.tree.node import Node

from .base import BaseConstraint


@dataclass(slots=True, frozen=True)
class Index(BaseConstraint):
    index: int

    @override
    def get_nodes(self) -> set[Node]:
        return set()

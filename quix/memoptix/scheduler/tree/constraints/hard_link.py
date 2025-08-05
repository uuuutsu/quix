from dataclasses import dataclass
from typing import override

from quix.memoptix.scheduler.tree.node import Node

from .base import BaseConstraint


@dataclass(slots=True, frozen=True)
class HardLink(BaseConstraint):
    to_: Node
    distance: int

    @override
    def get_nodes(self) -> set[Node]:
        return {
            self.to_,
        }

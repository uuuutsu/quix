from dataclasses import dataclass
from typing import override

from quix.memoptix.scheduler.owner import Owner

from .base import BaseConstraint


@dataclass(slots=True, frozen=True)
class LifeCycle(BaseConstraint):
    start: int
    end: int

    @override
    def get_owners(self) -> set[Owner]:
        return set()

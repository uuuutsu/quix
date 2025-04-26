from dataclasses import dataclass

from quix.memoptix.scheduler.owner import Owner

from .base import BaseConstraint


@dataclass(slots=True, frozen=True)
class Array(BaseConstraint):
    length: int

    def get_owners(self) -> set[Owner]:
        return set()

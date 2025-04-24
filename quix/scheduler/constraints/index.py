from dataclasses import dataclass

from quix.scheduler.owner import Owner

from .base import BaseConstraint


@dataclass(slots=True, frozen=True)
class Index(BaseConstraint):
    index: int

    def get_owners(self) -> set[Owner]:
        return set()

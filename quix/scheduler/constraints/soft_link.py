from dataclasses import dataclass
from typing import override

from quix.scheduler.owner import Owner

from .base import BaseConstraint


@dataclass(slots=True, frozen=True)
class SoftLink(BaseConstraint):
    to_: dict[Owner, int]

    @override
    def get_owners(self) -> set[Owner]:
        return set(self.to_.keys())

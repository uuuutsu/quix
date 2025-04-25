from dataclasses import dataclass
from typing import override

from quix.scheduler.owner import Owner

from .base import BaseConstraint


@dataclass(slots=True, frozen=True)
class HardLink(BaseConstraint):
    to_: Owner
    distance: int

    @override
    def get_owners(self) -> set[Owner]:
        return {
            self.to_,
        }

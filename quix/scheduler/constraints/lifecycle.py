from dataclasses import dataclass

from .base import BaseConstraint


@dataclass(slots=True, frozen=True)
class LifeCycle(BaseConstraint):
    start: int
    end: int

from dataclasses import dataclass

from .base import BaseConstraint


@dataclass(slots=True, frozen=True)
class Index(BaseConstraint):
    index: int

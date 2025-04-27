from collections.abc import Hashable
from dataclasses import field

from quix.tools import generate_unique_id

from .base import DType, dtype


@dtype
class Unit(DType, Hashable):
    ref: int = field(default_factory=generate_unique_id)

    def __hash__(self) -> int:
        return self.ref

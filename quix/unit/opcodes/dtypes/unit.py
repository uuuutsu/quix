from collections.abc import Hashable
from dataclasses import field

from quix.core.opcodes.dtypes import Ref
from quix.tools import generate_unique_id

from .base import DType, dtype


@dtype
class Unit(DType, Hashable):
    ref: Ref = field(default_factory=generate_unique_id)

    def __hash__(self) -> int:
        return hash(self.ref)

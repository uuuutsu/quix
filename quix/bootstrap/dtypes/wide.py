from __future__ import annotations

from collections.abc import Iterator

from .base import DType, dtype
from .unit import Unit


@dtype
class Wide(DType):
    units: tuple[Unit, ...]

    def __iter__(self) -> Iterator[Unit]:
        return self.units.__iter__()

    def __len__(self) -> int:
        return len(self.units)

    @classmethod
    def from_length(cls, name: str, length: int) -> Wide:
        units = []
        for idx in range(length):
            units.append(Unit(f"{name}_{idx}"))
        return cls(name, tuple(units))

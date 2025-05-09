from __future__ import annotations

from collections.abc import Iterator
from typing import overload

from .base import DType, dtype
from .unit import Unit


@dtype
class Wide(DType):
    units: tuple[Unit, ...]

    def __post_init__(self) -> None:
        if len(set(self.units)) < len(self.units):
            raise ValueError(f"All units of {type(self).__name__!r} must be unique.")

    def __iter__(self) -> Iterator[Unit]:
        return self.units.__iter__()

    def __len__(self) -> int:
        return len(self.units)

    @overload
    def __getitem__(self, item: int) -> Unit: ...
    @overload
    def __getitem__(self, item: slice) -> tuple[Unit, ...]: ...
    def __getitem__(self, item: int | slice) -> Unit | tuple[Unit, ...]:
        return self.units[item]

    @property
    def size(self) -> int:
        return len(self)

    @classmethod
    def from_length(cls, name: str, length: int) -> Wide:
        units = []
        for idx in range(length):
            units.append(Unit(f"{name}_{idx}"))
        return cls(name, tuple(units))

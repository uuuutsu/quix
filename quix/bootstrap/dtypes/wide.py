from collections.abc import Iterable

from .base import DType, dtype
from .unit import Unit


@dtype
class Wide(DType):
    units: tuple[Unit, ...]

    def __iter__(self) -> Iterable[Unit]:
        return self.units.__iter__()

    def __len__(self) -> int:
        return len(self.units)

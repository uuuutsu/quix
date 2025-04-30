from .base import dtype
from .unit import Unit


@dtype
class Array(Unit):
    length: int = 256
    granularity: int = 0

    @property
    def full_length(self) -> int:
        return self.length * (self.granularity + 1)

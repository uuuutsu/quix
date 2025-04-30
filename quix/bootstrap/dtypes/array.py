from .base import dtype
from .unit import Unit


@dtype
class Array(Unit):
    length: int = 256
    granularity: int = 1

    @property
    def full_length(self) -> int:
        # N partitions + 1 control partition
        # each partition => [0][data1, data2, ...] => 1 + granularity
        return (self.length + 1) * (self.granularity + 1)

from typing import Final, override

from quix.bootstrap.dtypes.array import Array
from quix.bootstrap.dtypes.const import DynamicUInt
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocodes import init_array, load_array, store_array
from quix.bootstrap.program import ToConvert, convert
from quix.memoptix import index

from .component import Component

_DEFAULT_SIZE: Final[int] = 84000


class Memory(Component):
    __slots__ = "_array"

    def __init__(self, size_bytes: int = _DEFAULT_SIZE) -> None:
        self._array = Array("memory", length=size_bytes)

    @convert
    @override
    def create(self, memory_index: int) -> ToConvert:
        yield init_array(self._array)
        yield index(self._array, memory_index)
        return None

    @override
    def size(self) -> int:
        return self._array.full_length

    @convert
    def store(self, idx: DynamicUInt | Wide, value: DynamicUInt | Wide) -> ToConvert:
        return store_array(self._array, value, idx)

    @convert
    def load(self, idx: DynamicUInt | Wide, load_in: Wide) -> ToConvert:
        return load_array(self._array, load_in, idx)

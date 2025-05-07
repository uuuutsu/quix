from typing import Final, override

from quix.bootstrap.dtypes.array import Array
from quix.bootstrap.macrocodes import init_array
from quix.bootstrap.program import ToConvert, convert
from quix.memoptix import index

from .component import Component

_DEFAULT_SIZE_WORDS: Final[int] = 16384 // 4


class Memory(Component):
    __slots__ = "_array"

    def __init__(self, size_word: int = _DEFAULT_SIZE_WORDS) -> None:
        self._array = Array("memory", length=size_word, granularity=4)

    @convert
    @override
    def create(self, memory_index: int) -> ToConvert:
        yield init_array(self._array)
        yield index(self._array, memory_index)
        return None

    @override
    def size(self) -> int:
        return self._array.full_length

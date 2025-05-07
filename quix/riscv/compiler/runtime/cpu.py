from typing import override

from quix.bootstrap.dtypes.array import Array
from quix.bootstrap.dtypes.const import DynamicUInt
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocodes import assign_wide, init_array, load_array, store_array
from quix.bootstrap.program import ToConvert, convert
from quix.memoptix.opcodes import index

from .component import Component


class CPU(Component):
    __slots__ = (
        "_registers",
        "_pc",
    )

    def __init__(self) -> None:
        self._registers = Array("registers", length=32, granularity=4)
        self._pc = Wide.from_length("pc", 4)

    @convert
    @override
    def create(self, memory_index: int) -> ToConvert:
        for idx, unit in enumerate(self._pc):
            yield index(unit, memory_index + idx)
        yield init_array(self._registers)
        yield index(self._registers, memory_index + 4)
        return None

    @override
    def size(self) -> int:
        return self._registers.full_length + 4

    @convert
    def set_pc(self, pc: DynamicUInt) -> ToConvert:
        return assign_wide(self._pc, pc)

    @convert
    def store_register(self, idx: DynamicUInt | Wide, value: DynamicUInt | Wide) -> ToConvert:
        return store_array(self._registers, value, idx)

    @convert
    def load(self, idx: DynamicUInt | Wide, load_in: Wide) -> ToConvert:
        return load_array(self._registers, load_in, idx)

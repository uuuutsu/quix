from typing import override

from quix.bootstrap.dtypes.array import Array
from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocodes import add_wide, assign_wide, init_array, load_array, store_array, switch_wide
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, end_loop, start_loop

from .component import Component


class CPU(Component):
    __slots__ = (
        "_registers",
        "_pc",
        "_exit",
    )

    def __init__(self) -> None:
        self._registers = Array("registers", length=32, granularity=4)
        self._pc = Wide.from_length("pc", 4)
        self.exit = Unit("exit")

    @convert
    @override
    def create(self, memory_index: int) -> ToConvert:
        # for idx, unit in enumerate(self._pc):
        # yield index(unit, memory_index + idx)
        yield init_array(self._registers)
        # yield index(self._registers, memory_index + 4)
        return None

    @override
    def size(self) -> int:
        return self._registers.full_length + 4

    @convert
    def set_pc(self, pc: UDynamic) -> ToConvert:
        return assign_wide(self._pc, pc)

    @convert
    def next(self) -> ToConvert:
        return add_wide(self._pc, UDynamic.from_int(4, 4), self._pc)

    @convert
    def run(self, mapping: dict[UDynamic, ToConvert]) -> ToConvert:
        yield add(self.exit, 1)
        yield start_loop(self.exit)
        yield switch_wide(self._pc, mapping, else_=[add(self.exit, -1)])
        return end_loop()

    @convert
    def store_register(self, idx: UDynamic | Wide, value: UDynamic | Wide) -> ToConvert:
        return store_array(self._registers, value, idx)

    @convert
    def load_register(self, idx: UDynamic | Wide, load_in: Wide) -> ToConvert:
        return load_array(self._registers, load_in, idx)

    @property
    def pc(self) -> Wide:
        return self._pc

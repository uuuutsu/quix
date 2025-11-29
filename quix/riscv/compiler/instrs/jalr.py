from quix.bootstrap.dtypes.const import UCell, UDynamic
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import add_wide, and_unit, assign_unit, assign_wide
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.opcodes import add
from quix.memoptix.opcodes import free


@macrocode
def riscv_jalr(imm: UDynamic, rs1: Wide, rd: Wide, pc: Wide) -> ToConvert:
    yield assign_wide(rd, pc)
    yield add_wide(rd, UDynamic.from_int(4, 4), rd)
    yield assign_wide(pc, rs1)
    yield add_wide(pc, imm, pc)
    mask = Unit("mask")
    yield assign_unit(mask, UCell.from_value(0b11111110))
    yield and_unit(pc[0], mask, pc[0])
    yield add(mask, 2)
    return free(mask)

from quix.bootstrap.dtypes.array import Array
from quix.bootstrap.dtypes.const import UCell, UDynamic
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import add_wide, assign_unit, call_ge_unit, clear_unit, clear_wide, load_array, not_unit
from quix.bootstrap.macrocodes.nop import NOP
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.opcodes import add
from quix.memoptix.opcodes import free


@macrocode
def riscv_lb(imm: UDynamic, rs1: Wide, rd: Wide, memory: Array) -> ToConvert:
    yield add_wide(imm, rs1, rs1)
    yield clear_wide(Wide("rd_upper", rd[1:]))
    yield load_array(memory, Wide("lsb", (rd[0],)), rs1)
    lim = Unit("lim")
    yield assign_unit(lim, UCell.from_value(128))
    yield call_ge_unit(
        rd[0],
        lim,
        macrocode(add(rd[1], -1), add(rd[2], -1), add(rd[3], -1), not_unit(rd[0], rd[0])),
        NOP,
    )
    yield clear_unit(lim), free(lim)
    return None

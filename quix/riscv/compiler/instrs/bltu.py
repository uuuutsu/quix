from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import add_wide, call_lt_wide
from quix.bootstrap.macrocodes.nop import NOP
from quix.bootstrap.program import ToConvert


@macrocode
def bltu(imm: UDynamic, rs1: Wide, rs2: Wide, pc: Wide) -> ToConvert:
    return call_lt_wide(
        rs1,
        rs2,
        add_wide(pc, imm, pc),
        NOP,
    )

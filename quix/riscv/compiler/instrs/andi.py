from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import and_wide, assign_wide
from quix.bootstrap.program import ToConvert


@macrocode
def riscv_andi(imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
    yield assign_wide(rd, imm)
    yield and_wide(rs1, rd, rd)
    return None

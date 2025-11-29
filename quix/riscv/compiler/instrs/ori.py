from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import assign_wide, or_wide
from quix.bootstrap.program import ToConvert


@macrocode
def riscv_ori(imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
    yield assign_wide(rd, imm)
    yield or_wide(rs1, rd, rd)
    return None

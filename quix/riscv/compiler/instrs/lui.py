from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import assign_wide
from quix.bootstrap.program import ToConvert


@macrocode
def riscv_lui(imm: UDynamic, rd: Wide) -> ToConvert:
    yield assign_wide(rd, imm)
    return None

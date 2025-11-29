from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import add_wide, sub_wide
from quix.bootstrap.program import ToConvert

from .utils import is_signed


@macrocode
def riscv_addi(imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
    if is_signed(imm):
        yield sub_wide(rs1, imm, rd)
    else:
        yield add_wide(rs1, imm, rd)
    return None

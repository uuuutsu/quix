from quix.bootstrap.dtypes.const import DynamicUInt
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocodes import add_wide, sub_wide
from quix.bootstrap.program import ToConvert, convert

from .utils import is_signed


@convert
def addi(imm: DynamicUInt, rs1: Wide, rd: Wide) -> ToConvert:
    if is_signed(imm):
        return sub_wide(rs1, imm, rd)
    return add_wide(rs1, imm, rd)

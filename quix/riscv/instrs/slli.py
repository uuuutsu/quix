from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import mul_wide
from quix.bootstrap.program import ToConvert


@macrocode
def slli(imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
    yield mul_wide(rs1, UDynamic.from_int(2 ** (int(imm) & 0x1F), 4), rd)
    return None

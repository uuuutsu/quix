from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import div_wide, mul_wide
from quix.bootstrap.program import ToConvert


@macrocode
def riscv_srl(rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
    yield mul_wide(UDynamic.from_int(2, 4), rs2, rs2)
    yield div_wide(
        rs1,
        rs2,
        quotient=rd,
        remainder=None,
    )
    return None

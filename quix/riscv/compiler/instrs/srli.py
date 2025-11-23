from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import div_wide
from quix.bootstrap.program import ToConvert
from quix.riscv.loader.decoder.utils import get_bit_section


@macrocode
def srli(imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
    if get_bit_section(int(imm), 10, 10):
        yield div_wide(
            rs1,
            UDynamic.from_int(2 ** (int(imm) & 0x1F), 4),
            quotient=rd,
            remainder=None,
        )
    else:
        yield div_wide(
            rs1,
            UDynamic.from_int(2 ** (int(imm) & 0x1F), 4),
            quotient=rd,
            remainder=None,
        )
    return None

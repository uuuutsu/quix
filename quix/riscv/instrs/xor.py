from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import xor_wide
from quix.bootstrap.program import ToConvert


@macrocode
def xor(rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
    yield xor_wide(rs1, rs2, rd)
    return None

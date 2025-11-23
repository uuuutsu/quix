from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import or_wide
from quix.bootstrap.program import ToConvert


@macrocode
def or_(rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
    yield or_wide(rs1, rs2, rd)
    return None

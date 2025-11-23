from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import add_wide, assign_wide
from quix.bootstrap.program import ToConvert


@macrocode
def jal(imm: UDynamic, rd: Wide, pc: Wide) -> ToConvert:
    yield assign_wide(rd, pc)
    yield add_wide(rd, UDynamic.from_int(4, 4), rd)
    return add_wide(pc, imm, pc)

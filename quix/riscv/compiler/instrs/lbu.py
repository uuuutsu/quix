from quix.bootstrap.dtypes.array import Array
from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import add_wide, clear_wide, load_array
from quix.bootstrap.program import ToConvert


@macrocode
def lbu(imm: UDynamic, rs1: Wide, rd: Wide, memory: Array) -> ToConvert:
    yield add_wide(imm, rs1, rs1)
    yield clear_wide(Wide("rd_upper", rd[1:]))
    yield load_array(memory, Wide("lsb", (rd[0],)), rs1)
    return None

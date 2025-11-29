from quix.bootstrap.dtypes.array import Array
from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import add_wide, store_array
from quix.bootstrap.program import ToConvert


@macrocode
def riscv_sb(imm: UDynamic, rs1: Wide, rs2: Wide, memory: Array) -> ToConvert:
    yield add_wide(rs1, imm, rs1)
    yield store_array(memory, Wide("lsb", (rs2[0],)), rs1)
    return None

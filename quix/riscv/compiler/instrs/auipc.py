from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import add_wide
from quix.bootstrap.program import ToConvert


@macrocode
def riscv_auipc(imm: UDynamic, rd: Wide, pc: Wide) -> ToConvert:
    yield add_wide(pc, imm, rd)
    return None

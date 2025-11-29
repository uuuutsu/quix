from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import assign_wide, call_lt_wide_signed
from quix.bootstrap.program import ToConvert


@macrocode
def riscv_slt(rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
    yield call_lt_wide_signed(
        rs1,
        rs2,
        assign_wide(rd, UDynamic.from_int(1, 4)),
        assign_wide(rd, UDynamic.from_int(1, 4)),
    )
    return None

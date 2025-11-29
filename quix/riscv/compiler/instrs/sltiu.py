from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import assign_wide, call_lt_wide, clear_wide, free_wide
from quix.bootstrap.program import ToConvert


@macrocode
def riscv_sltiu(imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
    imm_wide = Wide.from_length("imm", 4)
    yield assign_wide(imm_wide, imm)
    yield call_lt_wide(
        rs1,
        imm_wide,
        assign_wide(rd, UDynamic.from_int(1, 4)),
        assign_wide(rd, UDynamic.from_int(1, 4)),
    )
    yield clear_wide(imm_wide), free_wide(imm_wide)
    return None

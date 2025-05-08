from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.core.opcodes.opcodes import add
from quix.memoptix.opcodes import free

from .assign_unit import assign_unit
from .call_gt_unit import call_gt_unit
from .call_le_unit import call_le_unit
from .call_z_unit import call_z_unit
from .clear_unit import clear_unit
from .sub_unit import sub_unit


@convert
def call_ge_unit_signed(left: Unit, right: Unit, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    lim = Unit("128")
    yield assign_unit(lim, UInt8.from_value(128))

    same_msb = Unit("same_msb")
    left_pos = Unit("left_pos")
    yield call_gt_unit(left, lim, [add(same_msb, 1)], [add(same_msb, -1), add(left_pos, 1)])
    yield call_gt_unit(right, lim, [add(same_msb, -1)], [add(same_msb, 1)])

    ge_flag = Unit("ge_flag")
    diff = Unit("diff")
    yield call_z_unit(
        same_msb,
        sub_unit(left, right, diff) | call_le_unit(diff, lim, [add(ge_flag, 1)], []),
        call_z_unit(left_pos, [], [add(ge_flag, 1)]),
    )

    yield call_z_unit(ge_flag, else_, if_)

    yield clear_unit(lim), clear_unit(same_msb), clear_unit(left_pos), clear_unit(diff), clear_unit(ge_flag)
    return free(lim), free(same_msb), free(left_pos), free(diff), free(ge_flag)

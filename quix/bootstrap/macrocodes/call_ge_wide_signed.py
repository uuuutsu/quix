from quix.bootstrap.dtypes import Unit, Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.nop import NOP
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.base import CoreOpcode
from quix.core.opcodes.opcodes import add
from quix.memoptix.opcodes import free
from quix.tools import Arg, check

from .call_eq_unit import call_eq_unit
from .call_ge_unit import call_ge_unit
from .call_ge_unit_signed import call_ge_unit_signed
from .call_z_unit import call_z_unit


@macrocode
@check(Arg("left").size == Arg("right").size)
def call_ge_wide_signed(left: Wide, right: Wide, if_: CoreOpcode, else_: CoreOpcode) -> ToConvert:
    ge_flag = Unit(f"{left.name}_ge_{right.name}_flag")
    yield add(ge_flag, 1)

    msb_left = left[-1]
    msb_right = right[-1]

    yield call_ge_unit_signed(
        msb_left,
        msb_right,
        call_eq_unit(
            left[-1],
            right[-1],
            _recursive_call_ge_unit_flag(left.units[:-1], right.units[:-1], ge_flag),
            NOP,
        ),
        add(ge_flag, -1),
    )

    yield call_z_unit(ge_flag, else_, macrocode(add(ge_flag, -1), if_))
    return free(ge_flag)


@macrocode
def _recursive_call_ge_unit_flag(left: tuple[Unit, ...], right: tuple[Unit, ...], ge_flag: Unit) -> ToConvert:
    if (len(left) == 0) or (len(right) == 0):
        return None
    return call_ge_unit(
        left[-1],
        right[-1],
        call_eq_unit(
            left[-1],
            right[-1],
            _recursive_call_ge_unit_flag(left[:-1], right[:-1], ge_flag),
            NOP,
        ),
        add(ge_flag, -1),
    )

from quix.bootstrap.dtypes import Unit, Wide
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.core.opcodes.opcodes import add
from quix.memoptix.opcodes import free
from quix.tools import Arg, check

from .call_eq_unit import call_eq_unit
from .call_ge_unit import call_ge_unit
from .call_z_unit import call_z_unit


@convert
@check(Arg("left").size == Arg("right").size)
def call_ge_wide(left: Wide, right: Wide, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    ge_flag = Unit(f"{left.name}_ge_{right.name}_flag")

    yield add(ge_flag, 1)
    yield _recursive_call_ge_unit_flag(left.units, right.units, ge_flag)
    yield call_z_unit(ge_flag, else_, [add(ge_flag, -1), *if_])
    return free(ge_flag)


@convert
def _recursive_call_ge_unit_flag(left: tuple[Unit, ...], right: tuple[Unit, ...], ge_flag: Unit) -> ToConvert:
    if (len(left) == 0) or (len(right) == 0):
        return None
    return call_ge_unit(
        left[0],
        right[0],
        call_eq_unit(
            left[0],
            right[0],
            _recursive_call_ge_unit_flag(left[1:], right[1:], ge_flag),
            [],
        ),
        [add(ge_flag, -1)],
    )

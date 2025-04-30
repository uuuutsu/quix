from quix.bootstrap.dtypes import Unit, Wide
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.core.opcodes.opcodes import add
from quix.memoptix.opcodes import free
from quix.tools import Arg, check

from .call_neq_unit import call_neq_unit
from .call_z_unit import call_z_unit


@convert
@check(Arg("left").size == Arg("right").size)
def call_neq_wide(left: Wide, right: Wide, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    neq_flag = Unit(f"{left.name}_neq_{right.name}_flag")

    yield _recursive_call_neq_unit_flag(left.units, right.units, neq_flag)
    yield call_z_unit(neq_flag, else_, [add(neq_flag, -1), *if_])
    return free(neq_flag)


@convert
def _recursive_call_neq_unit_flag(left: tuple[Unit, ...], right: tuple[Unit, ...], neq_flag: Unit) -> ToConvert:
    if (len(left) == 0) or (len(right) == 0):
        return None
    return call_neq_unit(
        left[0],
        right[0],
        [add(neq_flag, 1)],
        _recursive_call_neq_unit_flag(left[1:], right[1:], neq_flag),
    )

from quix.bootstrap.dtypes import Wide
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.core.opcodes.opcodes import add
from quix.memoptix.opcodes import free

from .call_z_unit import call_z_unit


@convert
def call_z_wide(value: Wide, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    zero_flag = Unit(f"{value.name}_zero_flag")

    yield add(zero_flag, 1)
    yield _recursive_call_z_zero_flag(value.units, zero_flag)
    yield call_z_unit(zero_flag, else_, [add(zero_flag, -1), *if_])
    return free(zero_flag)


@convert
def _recursive_call_z_zero_flag(units: tuple[Unit, ...], zero_flag: Unit) -> ToConvert:
    if len(units) == 0:
        return None
    return call_z_unit(units[0], _recursive_call_z_zero_flag(units[1:], zero_flag), [add(zero_flag, -1)])

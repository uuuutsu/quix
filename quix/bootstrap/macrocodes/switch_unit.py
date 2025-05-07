from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.memoptix.opcodes import free

from .assign_unit import assign_unit
from .call_z_unit import call_z_unit
from .clear_unit import clear_unit
from .sub_unit import sub_unit


@convert
def switch_unit(value: Unit, branches: dict[UInt8, CoreProgram]) -> ToConvert:
    buff = Unit(f"{value.name}_buff")

    yield assign_unit(buff, value)

    sorted_keys = sorted(branches, key=lambda x: int(x))
    last_val = UInt8.from_value(0)
    for key in sorted_keys:
        yield sub_unit(buff, key - last_val, buff)
        yield call_z_unit(buff, branches[key], [])
        last_val = key

    yield clear_unit(buff)
    return free(buff)

from quix.bootstrap.dtypes.const import UCell
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.dtypes import CoreProgram
from quix.core.opcodes.opcodes import add
from quix.memoptix.opcodes import free

from .assign_unit import assign_unit
from .call_z_unit import call_z_unit
from .clear_unit import clear_unit
from .sub_unit import sub_unit


@macrocode
def switch_unit(value: Unit, branches: dict[UCell, CoreProgram], else_: CoreProgram) -> ToConvert:
    buff = Unit(f"{value.name}_buff")
    else_flag = Unit(f"{value.name}_else_flag")

    yield assign_unit(buff, value)

    sorted_keys = sorted(branches, key=lambda x: int(x))
    last_val = UCell.from_value(0)
    for key in sorted_keys:
        yield sub_unit(buff, key - last_val, buff)
        yield call_z_unit(buff, [*branches[key], add(else_flag, 1)], [])
        last_val = key

    yield call_z_unit(else_flag, else_, clear_unit(else_flag))

    yield clear_unit(buff)
    return free(buff), free(else_flag)

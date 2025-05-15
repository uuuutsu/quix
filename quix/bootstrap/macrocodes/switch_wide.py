from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.opcodes import add
from quix.memoptix.opcodes import free

from .assign_wide import assign_wide
from .call_z_unit import call_z_unit
from .call_z_wide import call_z_wide
from .clear_unit import clear_unit
from .clear_wide import clear_wide
from .free_wide import free_wide
from .sub_wide import sub_wide


@macrocode
def switch_wide(value: Wide, branches: dict[UDynamic, ToConvert], else_: ToConvert) -> ToConvert:
    buff = Wide.from_length(f"{value.name}_buff", value.size)
    else_flag = Unit(f"{value.name}_else_flag")

    yield assign_wide(buff, value)

    sorted_keys = sorted(branches, key=lambda x: int(x))
    last_val = UDynamic.from_int(0, value.size)
    for key in sorted_keys:
        yield sub_wide(buff, key - last_val, buff)
        yield call_z_wide(buff, [branches[key], add(else_flag, 1)], [])
        last_val = key

    yield call_z_unit(else_flag, else_, clear_unit(else_flag))

    yield clear_wide(buff)
    return free_wide(buff), free(else_flag)

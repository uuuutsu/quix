from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert

from .move_unit_carry import _recursive_carry_increment


@macrocode
def inc_wide(value: Wide) -> ToConvert:
    return _recursive_carry_increment(value[0], value[1:])

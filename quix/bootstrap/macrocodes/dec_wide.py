from quix.bootstrap.dtypes import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert

from .move_unit_carry import _recursive_carry_decrement


@macrocode
def dec_wide(value: Wide) -> ToConvert:
    return _recursive_carry_decrement(value[0], value[1:])

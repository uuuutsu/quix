from quix.bootstrap.dtypes import Wide
from quix.bootstrap.program import ToConvert, convert

from .move_unit_carry import _recursive_carry_decrement


@convert
def dec_wide(value: Wide) -> ToConvert:
    return _recursive_carry_decrement(value[0], value[1:])

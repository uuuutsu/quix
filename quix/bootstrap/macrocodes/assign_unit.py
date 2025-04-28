from quix.bootstrap.dtypes import Int8, UInt8, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add

from .clear_unit import clear_unit
from .copy_unit import copy_unit


@convert
def assign_unit(to: Unit, value: Unit | UInt8 | Int8) -> ToConvert:
    if isinstance(value, Unit):
        return clear_unit(to), copy_unit(value, {to: Int8.from_value(1)})

    to_assign: int = value.value
    if to_assign < 0:
        to_assign = abs(to_assign)
    if to_assign > 127:
        to_assign = -(256 - to_assign)

    return clear_unit(to), add(to, to_assign)

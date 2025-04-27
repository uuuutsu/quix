from quix.bootstrap.dtypes import Int8, UInt8, Unit
from quix.bootstrap.program import ToConvert, convert

from .copy_unit import copy_unit


@convert
def assign_unit[Literal: UInt8 | Int8](to: Unit, value: Unit | Literal) -> ToConvert:
    if isinstance(value, Unit):
        return copy_unit(value, {to: Int8.from_value(1)})

    return []

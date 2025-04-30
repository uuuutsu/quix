from quix.bootstrap.dtypes import DynamicInt, DynamicUInt, Int8, Unit, Wide
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.program import ToConvert, convert
from quix.tools import Arg, check

from .assign_unit import assign_unit


@convert
@check(Arg("to").size == Arg("value").size)
def assign_wide(
    to: Wide,
    value: Wide | DynamicUInt | DynamicInt,
) -> ToConvert:
    args: tuple[tuple[Unit, Unit | UInt8 | Int8]] = tuple(zip(to, value, strict=True))  # type: ignore

    for to_unit, value_unit in args:
        yield assign_unit(to_unit, value_unit)

    return None

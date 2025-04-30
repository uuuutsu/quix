from quix.bootstrap.dtypes import DynamicUInt, UInt8, Unit, Wide
from quix.bootstrap.program import ToConvert, convert
from quix.tools import Arg, check

from .not_unit import not_unit


@convert
@check(Arg("left").size == Arg("target").size)
def not_wide(left: Wide | DynamicUInt, target: Wide) -> ToConvert:
    left_unit: Unit | UInt8
    right_unit: Unit
    for left_unit, right_unit in zip(left, target, strict=True):  # type: ignore
        yield not_unit(left_unit, right_unit)
    return None

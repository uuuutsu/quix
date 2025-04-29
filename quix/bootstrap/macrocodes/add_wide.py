from quix.bootstrap.dtypes import DynamicUInt, Unit, Wide
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.program import ToConvert, convert
from quix.tools import Arg, check

from .add_unit_carry import add_unit_carry


@convert
@check(Arg("left").size == Arg("right").size == Arg("target").size)
def add_wide(
    left: Wide | DynamicUInt,
    right: Wide | DynamicUInt,
    target: Wide,
) -> ToConvert:
    left_unit: UInt8 | Unit
    right_unit: UInt8 | Unit
    for idx, (left_unit, right_unit, target_unit) in enumerate(zip(left, right, target, strict=True)):  # type: ignore
        yield add_unit_carry(left_unit, right_unit, target_unit, target[idx + 1 :])

    return None

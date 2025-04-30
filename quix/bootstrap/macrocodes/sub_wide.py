from quix.bootstrap.dtypes import DynamicUInt, Unit, Wide
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.program import ToConvert, convert
from quix.tools import Arg, check

from .sub_unit_carry import sub_unit_carry


@convert
@check(Arg("left").size == Arg("right").size == Arg("target").size)
def sub_wide(
    left: Wide | DynamicUInt,
    right: Wide | DynamicUInt,
    target: Wide,
) -> ToConvert:
    args: tuple[tuple[UInt8 | Unit, UInt8 | Unit, Unit]] = tuple(zip(left, right, target, strict=True))  # type: ignore
    # We must start adding from the end, to avoid zeroing carries
    inv_args = args[::-1]

    for idx, (left_unit, right_unit, target_unit) in enumerate(inv_args):
        yield sub_unit_carry(left_unit, right_unit, target_unit, target[-idx:] if idx > 0 else ())

    return None

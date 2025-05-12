from quix.bootstrap.dtypes import UDynamic, Unit, Wide
from quix.bootstrap.dtypes.const import UCell
from quix.bootstrap.program import ToConvert, convert
from quix.tools import Arg, check

from .add_unit_carry import add_unit_carry


@convert
@check(Arg("left").size == Arg("right").size == Arg("target").size)
def add_wide(
    left: Wide | UDynamic,
    right: Wide | UDynamic,
    target: Wide,
) -> ToConvert:
    args: tuple[tuple[UCell | Unit, UCell | Unit, Unit]] = tuple(zip(left, right, target, strict=True))  # type: ignore
    # We must start adding from the end, to avoid zeroing carries
    inv_args = args[::-1]

    for idx, (left_unit, right_unit, target_unit) in enumerate(inv_args):
        yield add_unit_carry(left_unit, right_unit, target_unit, target[-idx:] if idx > 0 else ())

    return None

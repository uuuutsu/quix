from quix.bootstrap.dtypes import UDynamic, Unit, Wide
from quix.bootstrap.dtypes.const import UCell
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.tools import Arg, check

from .mul_unit_carry import mul_unit_carry


@macrocode
@check(Arg("left").size == Arg("right").size == Arg("target").size)
def mul_wide_carry(
    left: Wide | UDynamic,
    right: Wide | UDynamic,
    target: Wide,
    carry: tuple[Unit, ...],
) -> ToConvert:
    args: tuple[tuple[UCell | Unit, UCell | Unit, Unit]] = tuple(zip(left, right, target, strict=True))  # type: ignore
    # We must start adding from the end, to avoid zeroing carries
    inv_args = args[::-1]

    for idx, (left_unit, right_unit, target_unit) in enumerate(inv_args):
        carry_default = target[-idx:] if idx > 0 else ()
        carry = carry_default + carry
        yield mul_unit_carry(left_unit, right_unit, target_unit, carry)

    return None

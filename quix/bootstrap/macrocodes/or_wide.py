from quix.bootstrap.dtypes import Unit, Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.tools import Arg, check

from .or_unit import or_unit


@macrocode
@check(Arg("left").size == Arg("right").size == Arg("target").size)
def or_wide(
    left: Wide,
    right: Wide,
    target: Wide,
) -> ToConvert:
    args: tuple[tuple[Unit, Unit, Unit]] = tuple(zip(left, right, target, strict=True))  # type: ignore

    for left_unit, right_unit, target_unit in args:
        yield or_unit(left_unit, right_unit, target_unit)

    return None

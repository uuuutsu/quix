from quix.bootstrap.dtypes import UCell, UDynamic, Unit, Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.tools import Arg, check

from .not_unit import not_unit


@macrocode
@check(Arg("left").size == Arg("target").size)
def not_wide(left: Wide | UDynamic, target: Wide) -> ToConvert:
    left_unit: Unit | UCell
    right_unit: Unit
    for left_unit, right_unit in zip(left, target, strict=True):  # type: ignore
        yield not_unit(left_unit, right_unit)
    return None

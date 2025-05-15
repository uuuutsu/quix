from quix.bootstrap.dtypes import Cell, UDynamic, Unit, Wide
from quix.bootstrap.dtypes.const import UCell
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.tools import Arg, check

from .assign_unit import assign_unit


@macrocode
@check(Arg("to").size == Arg("value").size)
def assign_wide(
    to: Wide,
    value: Wide | UDynamic,
) -> ToConvert:
    args: tuple[tuple[Unit, Unit | UCell | Cell]] = tuple(zip(to, value, strict=True))  # type: ignore

    for to_unit, value_unit in args:
        yield assign_unit(to_unit, value_unit)

    return None

from quix.bootstrap.dtypes import Cell, UDynamic, Unit, Wide
from quix.bootstrap.dtypes.const import UCell
from quix.bootstrap.program import ToConvert, convert
from quix.tools import Arg, check

from .assign_unit import assign_unit


@convert
@check(Arg("to").size == Arg("value").size)
def assign_wide(
    to: Wide,
    value: Wide | UDynamic,
) -> ToConvert:
    args: tuple[tuple[Unit, Unit | UCell | Cell]] = tuple(zip(to, value, strict=True))  # type: ignore

    for to_unit, value_unit in args:
        yield assign_unit(to_unit, value_unit)

    return None

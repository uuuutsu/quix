from quix.bootstrap.dtypes import Cell, UCell, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add

from .clear_unit import clear_unit
from .copy_unit import copy_unit


@convert
def assign_unit(to: Unit, value: Unit | UCell | Cell) -> ToConvert:
    if isinstance(value, Unit):
        return clear_unit(to), copy_unit(value, {to: Cell.from_value(1)})

    return clear_unit(to), add(to, Cell.wrap(value.value))

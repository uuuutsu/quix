from quix.bootstrap.dtypes import Cell, UCell, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add

from .assign_unit import assign_unit
from .clear_unit import clear_unit
from .copy_unit import copy_unit


@convert
def not_unit(left: Unit | UCell, target: Unit) -> ToConvert:
    if isinstance(left, UCell):
        return assign_unit(target, ~left)

    return _not_unit(left, target)


def _not_unit(left: Unit, target: Unit) -> ToConvert:
    if left == target:
        return copy_unit(left, {target: Cell.from_value(-2)}) | add(target, -1)

    return (
        clear_unit(target),
        add(target, -1),
        copy_unit(left, {target: Cell.from_value(-1)}),
    )

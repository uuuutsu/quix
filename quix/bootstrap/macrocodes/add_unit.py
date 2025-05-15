from quix.bootstrap.dtypes import Cell, UCell, Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add

from .clear_unit import clear_unit
from .copy_unit import copy_unit


@macrocode
def add_unit(left: Unit | UCell, right: Unit | UCell, target: Unit) -> ToConvert:
    if target == left:
        return _add_to_target(right, target)
    if target == right:
        return _add_to_target(left, target)

    return clear_unit(target) | _add_to_target(left, target) | _add_to_target(right, target)


@convert
def _add_to_target(argument: Unit | UCell, target: Unit) -> ToConvert:
    if isinstance(argument, UCell):
        return add(target, argument.value)

    return copy_unit(argument, {target: Cell.from_value(1)})

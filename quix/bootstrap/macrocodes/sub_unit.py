from quix.bootstrap.dtypes import UCell, Unit
from quix.bootstrap.dtypes.const import Cell
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.add_unit import add_unit
from quix.bootstrap.macrocodes.copy_unit import copy_unit
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.opcodes import add

from .clear_unit import clear_unit


@macrocode
def sub_unit(left: Unit | UCell, right: Unit | UCell, target: Unit) -> ToConvert:
    if target == left:
        return _sub_from_target(right, target=target)

    return _clear_and_sub(right, target), add_unit(target, left, target)


def _clear_and_sub(value: Unit | UCell, target: Unit) -> ToConvert:
    if isinstance(value, Unit) and (value == target):
        return clear_unit(target)

    return [
        clear_unit(target),
        _sub_from_target(value, target),
    ]


def _sub_from_target(value: Unit | UCell, target: Unit) -> ToConvert:
    if isinstance(value, UCell):
        return add(target, -value.value)

    return copy_unit(value, {target: Cell.from_value(-1)})

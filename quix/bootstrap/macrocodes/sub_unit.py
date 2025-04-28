from quix.bootstrap.dtypes import UInt8, Unit
from quix.bootstrap.dtypes.const import Int8
from quix.bootstrap.macrocodes.add_unit import add_unit
from quix.bootstrap.macrocodes.copy_unit import copy_unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add

from .clear_unit import clear_unit


@convert
def sub_unit(left: Unit | UInt8, right: Unit | UInt8, target: Unit) -> ToConvert:
    if target == left:
        return _sub_from_target(right, target=target)

    return _clear_and_sub(right, target), add_unit(target, left, target)


def _clear_and_sub(value: Unit | UInt8, target: Unit) -> ToConvert:
    if isinstance(value, Unit) and (value == target):
        return clear_unit(target)

    return [
        clear_unit(target),
        _sub_from_target(value, target),
    ]


def _sub_from_target(value: Unit | UInt8, target: Unit) -> ToConvert:
    if isinstance(value, UInt8):
        return add(target, -value.value)

    return copy_unit(value, {target: Int8.from_value(-1)})

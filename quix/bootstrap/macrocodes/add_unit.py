from quix.bootstrap.dtypes import Int8, UInt8, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add

from .clear_unit import clear_unit
from .copy_unit import copy_unit


@convert
def add_unit(left: Unit | UInt8, right: Unit | UInt8, target: Unit) -> ToConvert:
    if target == left:
        return _add_to_target(right, target)
    if target == right:
        return _add_to_target(left, target)

    return clear_unit(target) | _add_to_target(left, target) | _add_to_target(right, target)


def _add_to_target(argument: Unit | UInt8, target: Unit) -> ToConvert:
    if isinstance(argument, UInt8):
        return add(target, argument.value)

    return copy_unit(argument, {target: Int8.from_value(1)})

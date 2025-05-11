from quix.bootstrap.dtypes import Int8, UInt8, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, end_loop, start_loop
from quix.memoptix.opcodes import free

from .add_unit import add_unit
from .assign_unit import assign_unit
from .clear_unit import clear_unit
from .copy_unit import copy_unit
from .move_unit import move_unit


@convert
def mul_unit(left: Unit | UInt8, right: Unit | UInt8, target: Unit) -> ToConvert:
    if isinstance(left, UInt8) and isinstance(right, UInt8):
        return assign_unit(target, left * right)
    elif isinstance(right, UInt8):
        return _mul_by_int(left, right, target)  # type: ignore
    elif isinstance(left, UInt8):
        return _mul_by_int(right, left, target)

    return _mul_two_units(left, right, target)


def _mul_by_int(
    left: Unit,
    right: UInt8,
    target: Unit,
) -> ToConvert:
    if left == target:
        return copy_unit(left, {target: (right - 1).to(Int8)})

    return clear_unit(target) | copy_unit(left, {target: right.to(Int8)})


def _mul_two_units(
    left: Unit,
    right: Unit,
    target: Unit,
) -> ToConvert:
    left_buff, right_buff = Unit(f"{left.name}_buff"), Unit(f"{right.name}_buff")

    if left == right:
        yield move_unit(left, {left_buff: Int8.from_value(1), right_buff: Int8.from_value(1)})
    else:
        yield move_unit(left, {left_buff: Int8.from_value(1)})
        yield move_unit(right, {right_buff: Int8.from_value(1)})

    if target not in (left, right):
        yield clear_unit(target)

    yield start_loop(right_buff)
    yield add_unit(left_buff, target, target)
    if left != right != target:
        yield add(right, 1)
    yield add(right_buff, -1)
    yield end_loop()

    if left != target:
        yield move_unit(left_buff, {left: Int8.from_value(1)})
    else:
        yield clear_unit(left_buff)

    return [
        free(left_buff),
        free(right_buff),
    ]

from quix.bootstrap.dtypes import UInt8, Unit
from quix.bootstrap.dtypes.const import Int8
from quix.bootstrap.macrocodes.assign_unit import assign_unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, loop
from quix.memoptix.opcodes import free

from .add_unit_carry import add_unit_carry
from .clear_unit import clear_unit
from .move_unit import move_unit


@convert
def mul_unit_carry(
    left: Unit | UInt8,
    right: Unit | UInt8,
    target: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    if isinstance(right, UInt8) and isinstance(left, UInt8):
        return _mulc_ints(left, right, target, carry)
    elif isinstance(right, UInt8):
        return _mulc_by_int(left, right, target, carry)  # type: ignore
    elif isinstance(left, UInt8):
        return _mulc_by_int(right, left, target, carry)

    return _mulc_two_units(left, right, target, carry)


def _mulc_ints(
    left: UInt8,
    right: UInt8,
    target: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    left_buffer = Unit(f"{left.name}_buffer")
    yield assign_unit(left_buffer, left)
    yield _mulc_by_int(left_buffer, right, target, carry)
    yield clear_unit(left_buffer)
    return [free(left_buffer)]


def _mulc_by_int(
    left: Unit,
    right: UInt8,
    target: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    buffer = Unit("buffer")
    yield assign_unit(buffer, right)
    yield _mulc_two_units(left, buffer, target, carry)
    yield clear_unit(buffer)
    return free(buffer)


def _mulc_two_units(
    left: Unit,
    right: Unit,
    target: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    left_buff, right_buff = Unit(f"{left.name}_buffer"), Unit(f"{right.name}_buffer")

    if left == right:
        yield move_unit(left, {left_buff: Int8.from_value(1), right_buff: Int8.from_value(1)})
    else:
        yield move_unit(left, {left_buff: Int8.from_value(1)})
        yield move_unit(right, {right_buff: Int8.from_value(1)})

    if target not in (left, right):
        yield clear_unit(target)

    instrs = add_unit_carry(left_buff, target, target, carry=carry)
    if left != right != target:
        instrs |= add(right, 1)
    instrs |= add(right_buff, -1)
    yield loop(right_buff, instrs)

    if left != target:
        yield move_unit(left_buff, {left: Int8.from_value(1)})
    else:
        yield clear_unit(left_buff)

    return [free(left_buff), free(right_buff)]

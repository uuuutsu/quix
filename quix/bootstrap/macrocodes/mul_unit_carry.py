from quix.bootstrap.dtypes import UCell, Unit
from quix.bootstrap.dtypes.const import Cell
from quix.bootstrap.macrocodes.assign_unit import assign_unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, end_loop, start_loop
from quix.memoptix.opcodes import free

from .add_unit_carry import add_unit_carry
from .clear_unit import clear_unit
from .move_unit import move_unit


@convert
def mul_unit_carry(
    left: Unit | UCell,
    right: Unit | UCell,
    target: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    if isinstance(right, UCell) and isinstance(left, UCell):
        return _mulc_ints(left, right, target, carry)
    elif isinstance(right, UCell):
        return _mulc_by_int(left, right, target, carry)  # type: ignore
    elif isinstance(left, UCell):
        return _mulc_by_int(right, left, target, carry)

    return _mulc_two_units(left, right, target, carry)


def _mulc_ints(
    left: UCell,
    right: UCell,
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
    right: UCell,
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
        yield move_unit(left, {left_buff: Cell.from_value(1), right_buff: Cell.from_value(1)})
    else:
        yield move_unit(left, {left_buff: Cell.from_value(1)})
        yield move_unit(right, {right_buff: Cell.from_value(1)})

    if target not in (left, right):
        yield clear_unit(target)

    yield start_loop(right_buff)
    yield add_unit_carry(left_buff, target, target, carry=carry)
    if left != right != target:
        yield add(right, 1)
    yield add(right_buff, -1)
    yield end_loop()

    if left != target:
        yield move_unit(left_buff, {left: Cell.from_value(1)})
    else:
        yield clear_unit(left_buff)

    return [free(left_buff), free(right_buff)]

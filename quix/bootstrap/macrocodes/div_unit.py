from quix.bootstrap.dtypes import UCell, Unit
from quix.bootstrap.dtypes.const import Cell
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, end_loop, start_loop
from quix.memoptix.opcodes import free

from .assign_unit import assign_unit
from .call_z_unit import call_z_unit
from .clear_unit import clear_unit
from .move_unit import move_unit


@convert
def div_unit(
    left: Unit | UCell,
    right: Unit | UCell,
    quotient: Unit | None,
    remainder: Unit | None,
) -> ToConvert:
    if remainder is quotient is None:
        return None
    elif remainder == quotient:
        raise ValueError("Remainder cannot be Quotient")
    elif isinstance(left, UCell) and isinstance(right, UCell):
        return _div_ints(left, right, quotient, remainder)
    elif left == right:
        return _div_by_itself(quotient, remainder)

    return _div_units_and_ints(left, right, quotient, remainder)


def _div_ints(
    left: UCell,
    right: UCell,
    quotient: Unit | None,
    remainder: Unit | None,
) -> ToConvert:
    quot_int, rem_int = divmod(left, right)

    if quotient:
        yield assign_unit(quotient, quot_int)

    if remainder:
        yield assign_unit(remainder, rem_int)

    return None


def _div_by_itself(
    quotient: Unit | None,
    remainder: Unit | None,
) -> ToConvert:
    if quotient:
        yield assign_unit(quotient, UCell.from_value(1))

    if remainder:
        yield clear_unit(remainder)

    return None


def _div_units_and_ints(
    left: Unit | UCell,
    right: Unit | UCell,
    quotient: Unit | None,
    remainder: Unit | None,
) -> ToConvert:
    rem_buff, left_buff = Unit("rem_buff"), Unit("left_buff")

    dynamic_right: bool = False
    if isinstance(right, UCell):
        right_unit = Unit("right_unit")
        yield assign_unit(right_unit, right)
        dynamic_right = True
    elif right in [quotient, remainder]:
        right_unit = Unit("right_unit")
        yield move_unit(right, {right_unit: Cell.from_value(1)})
        dynamic_right = True
    else:
        right_unit = right

    if isinstance(left, UCell):
        yield assign_unit(left_buff, left)
    else:
        yield move_unit(left, {left_buff: Cell.from_value(1)})

    if quotient:
        yield clear_unit(quotient)

    yield start_loop(left_buff)
    yield add(left_buff, -1), add(right_unit, -1), add(rem_buff, 1)

    if (left not in (remainder, quotient)) and isinstance(left, Unit):
        yield add(left, 1)
    if_ = move_unit(rem_buff, {right_unit: Cell.from_value(1)})
    if quotient:
        if_ |= add(quotient, 1)
    yield call_z_unit(right_unit, if_, [])
    yield end_loop()

    if dynamic_right:
        yield clear_unit(right_unit), free(right_unit)

    if remainder:
        yield clear_unit(remainder)

    if remainder and not dynamic_right:
        yield move_unit(rem_buff, {right_unit: Cell.from_value(1), remainder: Cell.from_value(1)})
    elif remainder:
        yield move_unit(rem_buff, {remainder: Cell.from_value(1)})
    elif not dynamic_right:
        yield move_unit(rem_buff, {right_unit: Cell.from_value(1)})
    else:
        yield clear_unit(rem_buff)

    return [free(rem_buff), free(left_buff)]

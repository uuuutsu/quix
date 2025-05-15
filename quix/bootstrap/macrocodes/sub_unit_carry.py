from quix.bootstrap.dtypes import UCell, Unit
from quix.bootstrap.dtypes.const import Cell
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.call_z_unit import call_z_unit
from quix.bootstrap.macrocodes.clear_unit import clear_unit
from quix.bootstrap.macrocodes.copy_unit import copy_unit
from quix.bootstrap.program import ToConvert
from quix.memoptix.opcodes import free

from .add_unit_carry import add_unit_carry
from .assign_unit import assign_unit
from .move_unit import move_unit
from .move_unit_carry import _recursive_carry_decrement, move_unit_carry
from .sub_unit import _sub_from_target


@macrocode
def sub_unit_carry(
    left: Unit | UCell,
    right: Unit | UCell,
    target: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    if target == left:
        return _subc_from_target(right, target, carry)

    yield _clear_target_and_sub_carry(right, target, carry)
    return add_unit_carry(left, target, target, carry)


def _clear_target_and_sub_carry(value: Unit | UCell, target: Unit, carry: tuple[Unit, ...]) -> ToConvert:
    if isinstance(value, Unit) and (value == target):
        yield call_z_unit(
            value,
            [],
            else_=_recursive_carry_decrement(carry[0], carry[1:]),
        )
        return copy_unit(value, {target: Cell.from_value(-3)})

    yield clear_unit(target)

    if isinstance(value, UCell) and (value.value != 0) and carry:
        yield _recursive_carry_decrement(carry[0], carry[1:])
    elif isinstance(value, Unit) and carry:
        yield call_z_unit(
            value,
            [],
            _recursive_carry_decrement(carry[0], carry[1:]),
        )

    return _sub_from_target(value, target)


def _subc_from_target(
    right: Unit | UCell,
    target: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    if isinstance(right, UCell):
        buffer = Unit("buffer")

        yield assign_unit(buffer, right)
        yield move_unit_carry(buffer, {target: Cell.from_value(-1)}, {target: carry})
        return free(buffer)

    return _move_without_clear_with_carry_decrement(right, target, carry)


def _move_without_clear_with_carry_decrement(
    from_: Unit,
    to_: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    if from_ == to_:
        return clear_unit(to_)

    buffer = Unit("buffer")
    yield move_unit(from_, {buffer: Cell.from_value(1)})
    yield move_unit_carry(buffer, {from_: Cell.from_value(1), to_: Cell.from_value(-1)}, {to_: carry})
    return free(buffer)

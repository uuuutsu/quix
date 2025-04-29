from quix.bootstrap.dtypes import UInt8, Unit
from quix.bootstrap.dtypes.const import Int8
from quix.bootstrap.program import ToConvert, convert
from quix.memoptix.opcodes import free

from .assign_unit import assign_unit
from .clear_unit import clear_unit
from .move_unit import move_unit
from .move_unit_carry import move_unit_carry


@convert
def add_unit_carry(
    left: Unit | UInt8,
    right: Unit | UInt8,
    target: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    if target == left:
        return _addc_to_target(right, target, carry)
    elif target == right:
        return _addc_to_target(left, target, carry)

    return clear_unit(target), _addc_to_target(left, target, carry), _addc_to_target(right, target, carry)


def _addc_to_target(argument: Unit | UInt8, target: Unit, carry: tuple[Unit, ...]) -> ToConvert:
    if isinstance(argument, UInt8):
        buffer = Unit("buffer")

        yield assign_unit(buffer, argument)
        yield move_unit_carry(buffer, {target: Int8.from_value(1)}, {target: carry})
        return free(buffer)

    return _move_without_clear_with_carry_increment(argument, target, carry)


def _move_without_clear_with_carry_increment(
    from_: Unit,
    to_: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    buffer = Unit("buffer")
    yield move_unit(from_, {buffer: Int8.from_value(1)})

    if from_ == to_:
        yield move_unit_carry(buffer, {from_: Int8.from_value(2)}, {to_: carry})
    else:
        yield move_unit_carry(buffer, {from_: Int8.from_value(1), to_: Int8.from_value(1)}, {to_: carry})
    return free(buffer)

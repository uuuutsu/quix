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
    augend: Unit | UInt8,
    addend: Unit | UInt8,
    target: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    if target == augend:
        return _addc_to_target(addend, target, carry)
    elif target == addend:
        return _addc_to_target(augend, target, carry)

    return clear_unit(target), _addc_to_target(augend, target, carry), _addc_to_target(addend, target, carry)


def _addc_to_target(argument: Unit | UInt8, target: Unit, carry: tuple[Unit, ...]) -> ToConvert:
    if isinstance(argument, UInt8):
        buffer = Unit("buffer")

        yield assign_unit(buffer, argument)
        yield move_unit_carry(buffer, {target: Int8.from_value(1)}, {target: carry})
        return free(buffer)

    return _move_without_clear_with_carry(argument, target, carry)


def _move_without_clear_with_carry(
    from_: Unit,
    to_: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    buffer = Unit("buffer")
    yield move_unit(from_, {buffer: Int8.from_value(1)})
    yield move_unit_carry(buffer, {from_: Int8.from_value(1), to_: Int8.from_value(1)}, {to_: carry})
    return free(buffer)

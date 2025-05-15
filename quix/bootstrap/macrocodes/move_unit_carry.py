from collections.abc import Callable

from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import Cell, UCell
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import SmartProgram, ToConvert, convert
from quix.core.opcodes import add
from quix.core.opcodes.opcodes import end_loop, start_loop
from quix.memoptix.opcodes import free

from .assign_unit import assign_unit
from .call_z_unit import call_z_unit


@macrocode
def move_unit_carry(value: Unit, to: dict[Unit, Cell], carries: dict[Unit, tuple[Unit, ...]]) -> ToConvert:
    if value in to:
        raise ValueError("Target set cannot contain origin `Unit`: {value}.")

    yield start_loop(value)
    yield add(value, -1)

    for unit, to_add in to.items():
        if value in carries.get(unit, ()):
            raise ValueError(f"Carry cannot reference origin: {value}")

        func: Callable[[Unit, tuple[Unit, ...]], SmartProgram]
        if to_add.value < 0:
            func = _recursive_carry_decrement
        else:
            func = _recursive_carry_increment

        if abs(to_add.value) <= 2:
            for _ in range(abs(to_add.value)):
                yield func(unit, carries.get(unit, ()))
        else:
            counter = Unit("counter")
            yield assign_unit(counter, UCell.from_value(abs(to_add.value)))
            yield start_loop(counter)
            yield add(counter, -1)
            yield func(unit, carries.get(unit, ()))
            yield end_loop()

            yield free(counter)

    return end_loop()


@convert
def _recursive_carry_increment(
    owner: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    if not carry:
        return add(owner, 1)

    yield add(owner, 1)
    return call_z_unit(owner, _recursive_carry_increment(carry[0], carry[1:]), [])


@convert
def _recursive_carry_decrement(
    owner: Unit,
    carry: tuple[Unit, ...],
) -> ToConvert:
    if not carry:
        return add(owner, -1)

    yield call_z_unit(owner, _recursive_carry_decrement(carry[0], carry[1:]), [])
    return add(owner, -1)

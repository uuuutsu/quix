from collections.abc import Callable

from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import Int8
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes import add, loop

from .call_z_unit import call_z_unit


@convert
def move_unit_carry(value: Unit, to: dict[Unit, Int8], carries: dict[Unit, tuple[Unit, ...]]) -> ToConvert:
    if value in to:
        raise ValueError("Target set cannot contain origin `Unit`: {value}.")

    instrs = [add(value, -1)]
    for unit, to_add in to.items():
        if value in carries.get(unit, ()):
            raise ValueError(f"Carry cannot reference origin: {value}")

        func: Callable[[Unit, tuple[Unit, ...]], ToConvert]
        if to_add.value < 0:
            func = _recursive_carry_decrement
        else:
            func = _recursive_carry_increment

        for _ in range(abs(to_add.value)):
            instrs.extend(func(unit, carries.get(unit, ())))

    return loop(value, instrs)


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

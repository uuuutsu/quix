from quix.bootstrap.dtypes import Cell, Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.core.opcodes import add
from quix.core.opcodes.opcodes import end_loop, start_loop


@macrocode
def move_unit(value: Unit, to: dict[Unit, Cell]) -> ToConvert:
    if value in to:
        raise ValueError("Target set cannot contain origin `Unit`: {value}.")

    yield start_loop(value)

    yield add(value, -1)
    for unit, scale in to.items():
        yield add(unit, scale.value)

    return end_loop()

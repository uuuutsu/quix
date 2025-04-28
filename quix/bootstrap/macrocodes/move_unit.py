from quix.bootstrap.dtypes import Int8, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes import add, loop


@convert
def move_unit(value: Unit, to: dict[Unit, Int8]) -> ToConvert:
    instrs = [add(value, -1)]

    if value in to:
        raise ValueError("Target set cannot contain origin `Unit`: {value}.")

    for unit, scale in to.items():
        instrs.append(add(unit, scale.value))

    return loop(value, instrs)

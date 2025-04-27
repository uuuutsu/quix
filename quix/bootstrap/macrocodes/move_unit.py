from quix.bootstrap.dtypes import Int8, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes import add, loop


@convert
def move_unit[Scale: Int8](value: Unit, to: dict[Unit, Scale]) -> ToConvert:
    instrs = [add(value, -1)]

    for unit, scale in to.items():
        instrs.append(add(unit, scale.value))

    return loop(value, instrs)

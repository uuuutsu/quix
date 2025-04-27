from quix.bootstrap.dtypes import Int8, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.memoptix.opcodes import free

from .move_unit import move_unit


@convert
def copy_unit[Scale: Int8](value: Unit, to: dict[Unit, Scale]) -> ToConvert:
    buff = Unit(f"{value.name}_buffer")

    return_scale = to.pop(value, Int8.from_value(0)).value + 1

    return [
        move_unit(value, {buff: Int8.from_value(1)}),
        move_unit(buff, {value: Int8.from_value(return_scale), **to}),
        free(buff),
    ]

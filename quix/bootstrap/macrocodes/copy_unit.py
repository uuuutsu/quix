from quix.bootstrap.dtypes import Int8, Unit
from quix.bootstrap.program import ToConvert, convert

from .move_unit import move_unit


@convert
def copy_unit[Scale: Int8](value: Unit, to: dict[Unit, Scale]) -> ToConvert:
    buff = Unit(f"{value.name}_buffer")

    if value in to:
        raise ValueError(f"Copy target cannot contain copy origin: {value}")

    return [
        move_unit(value, {buff: Int8.from_value(1)}),
        move_unit(buff, {value: Int8.from_value(1), **to}),
    ]

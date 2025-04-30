from quix.bootstrap.dtypes import Int8, Unit, Wide
from quix.bootstrap.dtypes.const import DynamicInt
from quix.bootstrap.program import ToConvert, convert

from .move_unit import move_unit


@convert
def move_wide(value: Wide, to: dict[Wide, DynamicInt]) -> ToConvert:
    for idx, unit_from in enumerate(value):
        target: dict[Unit, Int8] = {}
        for wide_to, scale in to.items():
            target[wide_to[idx]] = scale[idx]
        yield move_unit(unit_from, target)
    return None

from quix.bootstrap.dtypes import Int8, Unit, Wide
from quix.bootstrap.dtypes.const import DynamicInt
from quix.bootstrap.program import ToConvert, convert

from .copy_unit import copy_unit


@convert
def copy_wide(value: Wide, to: dict[Wide, DynamicInt]) -> ToConvert:
    for idx, unit_from in enumerate(value):
        target: dict[Unit, Int8] = {}
        for wide_to, scale in to.items():
            target[wide_to[idx]] = scale[idx]
        yield copy_unit(unit_from, target)
    return None

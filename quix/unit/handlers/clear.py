from quix.tools import dp_factory
from quix.unit.opcodes import Unit, Wide

from .utils import ToConvert, handler


@handler
def clear_wide(value: Wide) -> ToConvert:
    return [clear_unit(unit) for unit in set(value)]


@handler
def clear_unit(value: Unit) -> ToConvert:
    return value.to_var()("[-]")


clear = dp_factory("clear", clear_wide) | clear_unit

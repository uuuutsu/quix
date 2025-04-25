from quix.unit.opcodes import Unit, Wide

from .utils import ToConvert, handler


@handler
def clear(value: Wide) -> ToConvert:
    return [clear_unit(unit) for unit in set(value)]


def clear_unit(value: Unit) -> ToConvert:
    return value.to_var()("[-]", sortable=True)

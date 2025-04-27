from quix.bootstrap.dtypes import Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import inject


@convert
def clear_unit(value: Unit) -> ToConvert:
    return inject(value, "[-]", value, sortable=True)

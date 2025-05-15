from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.opcodes import inject


@macrocode
def clear_unit(value: Unit) -> ToConvert:
    return inject(value, "[-]", value, sortable=True)

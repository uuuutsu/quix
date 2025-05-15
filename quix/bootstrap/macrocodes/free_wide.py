from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.memoptix.opcodes import free


@macrocode
def free_wide(value: Wide) -> ToConvert:
    for unit in value:
        yield free(unit)
    return None

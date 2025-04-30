from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.program import ToConvert, convert
from quix.memoptix.opcodes import free


@convert
def free_wide(value: Wide) -> ToConvert:
    for unit in value:
        yield free(unit)
    return None

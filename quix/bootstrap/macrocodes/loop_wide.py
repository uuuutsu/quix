from quix.bootstrap.dtypes import Unit, Wide
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.core.opcodes.opcodes import add, loop
from quix.memoptix.opcodes import free

from .call_z_wide import call_z_wide


@convert
def loop_wide(value: Wide, program: CoreProgram) -> ToConvert:
    buffer = Unit(f"{value}_loop_flag")
    yield call_z_wide(value, [], [add(buffer, 1)])
    yield loop(
        buffer,
        [
            *program,
            *call_z_wide(value, [add(buffer, -1)], []),
        ],
    )
    return free(buffer)

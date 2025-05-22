from quix.bootstrap.dtypes import Unit, Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.opcodes import add, end_loop, start_loop
from quix.memoptix.opcodes import free

from .call_z_wide import call_z_wide


@macrocode
def loop_wide(value: Wide, program: ToConvert) -> ToConvert:
    buffer = Unit(f"{value.name}_loop_flag")
    new_buff = Unit("buffer")

    yield add(buffer, 1)

    yield start_loop(buffer)
    yield call_z_wide(value, add(buffer, -1), add(new_buff, 1), inline=True)

    yield start_loop(new_buff)
    yield program
    yield add(new_buff, -1)
    yield end_loop()

    yield end_loop()

    return free(buffer), free(new_buff)

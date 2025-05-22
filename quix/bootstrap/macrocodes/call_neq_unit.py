from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.clear_unit import clear_unit
from quix.bootstrap.macrocodes.sub_unit import sub_unit
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.base import CoreOpcode
from quix.core.opcodes.opcodes import add, end_loop, start_loop
from quix.memoptix.opcodes import free


@macrocode
def call_neq_unit(left: Unit, right: Unit, if_: CoreOpcode, else_: CoreOpcode) -> ToConvert:
    else_flag, buffer = Unit("else_flag"), Unit("buffer")

    yield sub_unit(left, right, buffer)
    yield add(else_flag, 1)

    yield start_loop(buffer)
    yield add(else_flag, -1)
    yield if_
    yield clear_unit(buffer)
    yield end_loop()

    yield start_loop(else_flag)
    yield add(else_flag, -1)
    yield else_
    yield end_loop()

    return [
        free(else_flag),
        free(buffer),
    ]

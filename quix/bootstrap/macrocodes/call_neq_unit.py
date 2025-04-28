from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocodes.clear_unit import clear_unit
from quix.bootstrap.macrocodes.sub_unit import sub_unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.core.opcodes.opcodes import add, loop
from quix.memoptix.opcodes import free


@convert
def call_neq_unit(left: Unit, right: Unit, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    else_flag, buffer = Unit("else_flag"), Unit("buffer")

    return [
        sub_unit(left, right, buffer),
        add(else_flag, 1),
        # If Not Equal
        loop(
            buffer,
            [
                add(else_flag, -1),
                *if_,
                *clear_unit(buffer),
            ],
        ),
        # If Equal
        loop(
            else_flag,
            [
                add(else_flag, -1),
                *else_,
            ],
        ),
        #
        free(else_flag),
        free(buffer),
    ]

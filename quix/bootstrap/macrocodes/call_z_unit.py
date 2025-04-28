from quix.bootstrap.dtypes import Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.core.opcodes.opcodes import add, inject
from quix.memoptix.opcodes import free, soft_link


@convert
def call_z_unit(value: Unit, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    else_flag, zero = Unit(f"{value.name}_else_z_flag"), Unit(f"{value.name}_zero")

    return [
        soft_link(value, {else_flag: 1, zero: 2}),
        #
        add(else_flag, 1),
        # IF Zero
        inject(value, "[", value),
        else_,
        inject(else_flag, "-]", value),
        # Else
        inject(else_flag, "[-", else_flag),
        if_,
        inject(zero, "]", zero),
        #
        free(else_flag),
        free(zero),
    ]

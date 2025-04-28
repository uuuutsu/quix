from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import Int8
from quix.bootstrap.macrocodes.call_z_unit import call_z_unit
from quix.bootstrap.macrocodes.clear_unit import clear_unit
from quix.bootstrap.macrocodes.move_unit import move_unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.core.opcodes.opcodes import add, loop
from quix.memoptix.opcodes import free


@convert
def call_ge_unit(left: Unit, right: Unit, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    else_flag = Unit("else_ge_flag")
    left_buffer, right_buffer = Unit(f"{left.name}_buffer"), Unit(f"{right.name}_buffer")

    return [
        move_unit(left, {left_buffer: Int8.from_value(1)}),
        move_unit(right, {right_buffer: Int8.from_value(1)}),
        #
        loop(
            right_buffer,
            [
                add(right_buffer, -1),
                add(right, 1),
                *call_z_unit(
                    left_buffer,
                    [
                        *move_unit(
                            right_buffer,
                            {right: Int8.from_value(1)},
                        ),
                        add(else_flag, 1),
                    ],
                    [
                        add(left_buffer, -1),
                        add(left, 1),
                    ],
                ),
            ],
        ),
        move_unit(left_buffer, {left: Int8.from_value(1)}),
        # If Statement
        call_z_unit(else_flag, if_, else_),
        # Clean Up
        clear_unit(else_flag),
        free(else_flag),
        free(left_buffer),
        free(right_buffer),
    ]

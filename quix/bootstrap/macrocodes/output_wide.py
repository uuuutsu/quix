from math import ceil, log

from quix.bootstrap.dtypes import Array, DynamicUInt, Unit, Wide
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, inject, output
from quix.memoptix.opcodes import free

from .assign_wide import assign_wide
from .call_z_unit import call_z_unit
from .clear_unit import clear_unit
from .clear_wide import clear_wide
from .div_wide import div_wide
from .free_wide import free_wide
from .init_array import init_array
from .loop_wide import loop_wide
from .store_array import _array_move_by_wide_index, _array_set_control_unit, _go_by_value, store_array


@convert
def output_wide(wide: Wide) -> ToConvert:
    # TODO: optimize
    # We can use custom array and modify `div_wide` to store remainder
    # in it automatically instead of using expensive `array_store`.

    output_size = ceil(log(wide.size * 8, 2))
    output_arr = Array(f"{wide.name}_output_array", length=output_size, granularity=1)
    yield init_array(output_arr)

    counter = Unit("counter")

    to_div = Wide.from_length(f"{wide.name}_to_div", wide.size)
    to_print = Wide.from_length("to_print", wide.size)
    yield assign_wide(to_div, wide)

    instrs = div_wide(to_div, DynamicUInt.from_int(10, to_div.size), to_div, to_print)
    instrs |= call_z_unit(
        to_print[0],
        [],
        store_array(output_arr, Wide("value", to_print[0:1]), Wide("index", (counter,))),
    )
    instrs |= add(counter, 1)
    yield loop_wide(to_div, instrs)
    yield add(counter, -1)

    yield _array_set_control_unit(output_arr)
    yield _array_move_by_wide_index(output_arr, Wide("index", (counter,)))
    yield add(output_arr, 1)

    yield inject(output_arr, "[", output_arr)
    yield add(output_arr, -1)
    yield _go_by_value(output_arr, 1)
    yield add(output_arr, 48)
    yield output(output_arr)
    yield clear_unit(output_arr)
    yield _go_by_value(output_arr, -output_arr.granularity - 2)
    yield add(output_arr, 1)
    yield inject(output_arr, "]", output_arr)

    yield clear_wide(to_print)
    yield clear_unit(counter)

    return free(output_arr), free_wide(to_div), free(counter), free_wide(to_print)

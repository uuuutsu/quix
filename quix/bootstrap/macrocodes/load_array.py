from quix.bootstrap.dtypes import Array
from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.opcodes import add, inject

from .assign_wide import assign_wide
from .clear_wide import clear_wide
from .consts import CONSTANT_AS_WIDE_WHEN_LT
from .free_wide import free_wide
from .store_array import (
    _array_move_by_wide_index,
    _array_set_control_unit,
    _create_sequence_left,
    _go_by_value,
    _move_from_origin_by_trace,
    _move_in_array,
    _move_to_origin_traceless,
    _move_to_origin_with_trace,
)


@macrocode
def load_array(array: Array, load_in: Wide, index: Wide | UDynamic) -> ToConvert:
    if isinstance(index, UDynamic) and int(index) > CONSTANT_AS_WIDE_WHEN_LT:
        index_buff = Wide.from_length(f"{index}_index_buff", index.size)
        yield assign_wide(index_buff, index)
        yield _load_array(array, load_in, index_buff)
        yield clear_wide(index_buff)
        return free_wide(index_buff)
    return _load_array(array, load_in, index)


@macrocode
def _load_array(array: Array, load_in: Wide, index: Wide | UDynamic) -> ToConvert:
    yield clear_wide(load_in)

    if isinstance(index, UDynamic):
        return _array_load_by_int(array, load_in, index)

    return _array_load_by_wide(array, load_in, index)


def _array_load_by_wide(array: Array, load_in: Wide, index: Wide) -> ToConvert:
    yield _array_set_control_unit(array)
    yield _array_move_by_wide_index(array, index)
    yield _move_wide_to_control_from_current_position(array, load_in)
    return _move_to_origin_traceless(array)


def _move_wide_to_control_from_current_position(array: Array, load_in: Wide) -> ToConvert:
    offset: int = 1
    for unit in load_in:
        yield _move_wide_to_control(array, unit, offset)

        if offset % array.granularity == 0:
            offset += 1
        offset += 1
    return None


def _move_wide_to_control(array: Array, unit: Unit, offset: int) -> ToConvert:
    width = array.granularity + 1

    yield _copy_in_array(array, offset, 0, width)

    yield _go_by_value(array, width)
    yield inject(array, "[", array)
    yield _move_to_control_from_value(array)
    yield _go_by_value(array, width)
    yield add(array, 1)
    yield _move_from_origin_by_trace(array)
    yield _go_by_value(array, -width)
    yield inject(array, "]", array)

    yield _move_to_origin_with_trace(array)
    yield _go_by_value(array, width)
    yield add(array, -1)
    yield _array_load_unit_from_array(array, unit, width)
    yield add(array, 1)
    yield _move_from_origin_by_trace(array)

    return _go_by_value(array, -width * 2)


def _move_to_control_from_value(array: Array) -> ToConvert:
    width = array.granularity + 1
    code = "[" + _create_sequence_left(width) + "+]-"
    return inject(array, code, array)


def _copy_in_array(array: Array, from_: int, buff: int, to: int) -> ToConvert:
    yield _move_in_array(array, from_, buff)
    return _move_in_array(array, buff, from_, to)


def _array_load_by_int(array: Array, load_in: Wide, index: UDynamic) -> ToConvert:
    offset: int = 1
    for unit in load_in:
        yield _array_load_unit_by_int(array, unit, index, offset)
        offset += 2 if offset % array.granularity == 0 else 1
    return None


def _array_load_unit_by_int(array: Array, unit: Unit, index: UDynamic, offset: int) -> ToConvert:
    abs_offset = (int(index) + 1) * (array.granularity + 1) + offset
    yield _go_by_value(array, abs_offset)

    yield inject(array, "[", array)
    yield add(array, -1)
    yield _go_by_value(array, -abs_offset)
    yield add(array, 1)
    yield add(unit, 1)
    yield _go_by_value(array, abs_offset)
    yield inject(array, "]", array)

    yield _go_by_value(array, -abs_offset)
    return _move_in_array(array, 0, abs_offset)


def _array_load_unit_from_array(array: Array, unit: Unit, offset: int) -> ToConvert:
    yield inject(array, "[", array)
    yield add(array, -1)
    yield _go_by_value(array, -offset)
    yield add(unit, 1)
    yield _go_by_value(array, offset)
    yield inject(array, "]", array)

    return None

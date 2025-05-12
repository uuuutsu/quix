from quix.bootstrap.dtypes import Array
from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, end_loop, inject, start_loop


@convert
def store_array(array: Array, to_store: Wide | UDynamic, index: Wide | UDynamic) -> ToConvert:
    if isinstance(index, UDynamic):
        return _array_store_by_int(array, to_store, index)

    return _array_store_by_wide(array, to_store, index)


def _array_store_by_wide(array: Array, to_store: Wide | UDynamic, index: Wide) -> ToConvert:
    if isinstance(to_store, UDynamic):
        return _array_store_int_by_wide(array, to_store, index)

    return _array_store_wide_by_wide(array, to_store, index)


def _array_store_wide_by_wide(array: Array, to_store: Wide, index: Wide) -> ToConvert:
    yield _array_set_control_unit(array)
    yield _array_move_by_wide_index(array, index)
    yield _store_wide_in_current_position(array, to_store)
    return _move_to_origin_traceless(array)


def _store_wide_in_current_position(array: Array, to_store: Wide) -> ToConvert:
    offset = 1
    default_safe_zone = (array.granularity + 1) * 2
    for unit in to_store:
        yield _store_value_at_current_position(array, unit, default_safe_zone)

        yield _go_by_value_forward(array, offset)
        yield inject(array, "[-]", array)
        yield _move_in_array(array, default_safe_zone - offset, 0)
        yield _go_by_value_backward(array, offset)

        if offset % array.granularity == 0:
            offset += 1
        offset += 1

    return None


def _array_store_int_by_wide(array: Array, to_store: UDynamic, index: Wide) -> ToConvert:
    yield _array_set_control_unit(array)
    yield _array_move_by_wide_index(array, index)
    yield _store_int_in_current_position(array, to_store)
    return _move_to_origin_traceless(array)


def _array_move_by_wide_index(array: Array, index: Wide) -> ToConvert:
    yield _array_move_by_unit(array, index[0])

    rollback = 0
    default_safe_zone = (array.granularity + 1) * 2

    step = array.granularity + 1
    for unit in index[1:]:
        yield _store_value_at_current_position(array, unit, default_safe_zone)
        yield _go_by_value_forward(array, default_safe_zone)
        rollback += default_safe_zone

        step *= 1 << 8
        yield _go_by_index_in_current_cell(array, step)

    return _go_by_value_backward(array, rollback)


def _store_value_at_current_position(array: Array, unit: Unit, offset: int) -> ToConvert:
    yield _go_by_value_forward(array, offset)
    yield inject(array, "[-]", array)
    yield _go_by_value_backward(array, offset)

    yield _move_to_origin_with_trace(array)
    yield _array_store_unit_in_array(array, unit, array.granularity + 1)
    return _move_value_from_control_by_trace(array, offset)


def _move_value_from_control_by_trace(array: Array, offset: int) -> ToConvert:
    assert offset != 0
    obj_offset = array.granularity + 1

    yield _go_by_value_forward(array, obj_offset)

    yield inject(array, "[", array)
    yield _move_from_origin_by_trace(array)

    yield _go_by_value_forward(array, offset - obj_offset)
    yield add(array, 1)
    yield _go_by_value_backward(array, offset)

    yield _move_to_origin_with_trace(array)
    yield _go_by_value_forward(array, obj_offset)
    yield add(array, -1)
    yield inject(array, "]", array)

    yield add(array, 1)
    yield _move_from_origin_by_trace(array)

    yield _go_by_value_forward(array, offset - obj_offset)
    yield add(array, -1)
    return _go_by_value_backward(array, offset)


def _move_from_origin_by_trace(array: Array) -> ToConvert:
    step = array.granularity + 1
    code = "[-" + _create_sequence_right(step) + "]"
    return inject(array, code, array)


def _move_to_origin_with_trace(array: Array) -> ToConvert:
    step = array.granularity + 1
    code = "+[" + _create_sequence_left(step) + "+]-"
    return inject(array, code, array)


def _move_to_origin_traceless(array: Array) -> ToConvert:
    step = array.granularity + 1
    code = "+[-" + _create_sequence_left(step) + "+]"
    return inject(array, code, array)


def _array_move_by_unit(array: Array, index: Unit) -> ToConvert:
    yield _array_store_unit_in_array(array, index, array.granularity + 1)
    yield _go_by_value_forward(array, array.granularity + 1)
    return _go_by_index_in_current_cell(array)


def _go_by_index_in_current_cell(array: Array, step: int | None = None, max: int | None = None) -> ToConvert:
    if step is None:
        step = array.granularity + 1
    if max is None:
        max = min(array.full_length // step, 256)

    step_left = "[-"
    step_right = _create_sequence_right(step) + "]"
    code = step_left * max + step_right * max

    return inject(array, code, array)


@convert
def _array_set_control_unit(array: Array) -> ToConvert:
    return add(array, -1)


def _array_store_by_int(array: Array, to_store: Wide | UDynamic, index: UDynamic) -> ToConvert:
    if isinstance(to_store, UDynamic):
        return _array_store_int_by_int(array, to_store, index)

    return _array_store_wide_by_int(array, to_store, index)


def _array_store_wide_by_int(array: Array, to_store: Wide, index: UDynamic) -> ToConvert:
    offset: int = 1
    for unit in to_store:
        yield _array_store_unit_by_int(array, unit, index, offset)
        offset += 2 if offset % array.granularity == 0 else 1

    return None


def _array_store_unit_by_int(array: Array, unit: Unit, index: UDynamic, offset: int) -> ToConvert:
    return _array_store_unit_in_array(array, unit, (int(index) + 1) * (array.granularity + 1) + offset, clear=True)


def _move_in_array(array: Array, from_: int, *tos_: int) -> ToConvert:
    yield _go_by_value(array, from_)

    yield start_loop(array)
    yield add(array, -1)

    last = from_
    for to in tos_:
        yield _go_by_value(array, to - last)
        yield add(array, 1)
        last = to
    yield _go_by_value(array, from_ - last)
    yield end_loop()

    return _go_by_value(array, -from_)


def _go_by_value(array: Array, value: int) -> ToConvert:
    if value < 0:
        return _go_by_value_backward(array, abs(value))
    return _go_by_value_forward(array, value)


def _array_store_unit_in_array(array: Array, unit: Unit, offset: int, clear: bool = False) -> ToConvert:
    if offset == 1:
        buff, target = array.granularity + 1, offset
    else:
        buff, target = 1, offset

    if clear:
        yield _go_by_value_forward(array, target)
        yield inject(array, "[-]", array)
        yield _go_by_value_backward(array, target)

    yield start_loop(unit)
    yield add(unit, -1)
    yield _go_by_value_forward(array, buff)
    yield add(array, 1)
    yield _go_by_value_backward(array, buff)
    yield _go_by_value_forward(array, target)
    yield add(array, 1)
    yield _go_by_value_backward(array, target)
    yield end_loop()

    yield _go_by_value_forward(array, buff)
    yield inject(array, "[", array)
    yield add(array, -1)
    yield _go_by_value_backward(array, buff)
    yield add(unit, 1)
    yield _go_by_value_forward(array, buff)
    yield inject(array, "]", array)

    return _go_by_value_backward(array, buff)


def _array_store_int_by_int(array: Array, to_store: UDynamic, index: UDynamic) -> ToConvert:
    yield _go_by_index_forward(array, index)
    yield _store_int_in_current_position(array, to_store)
    return _go_by_index_backward(array, index)


def _store_int_in_current_position(array: Array, to_store: UDynamic) -> ToConvert:
    offset: int = 0
    for idx, value in enumerate(to_store):
        if idx and (idx % array.granularity == 0):
            yield _go_by_value_forward(array, 1)
            offset += 1
        offset += 1

        yield _go_by_value_forward(array, 1)
        yield inject(array, "[-]", array)
        yield add(array, value.value)

    return _go_by_value_backward(array, offset)


def _go_by_index_backward(array: Array, index: UDynamic, start_offset: int = 0) -> ToConvert:
    return _go_by_value_backward(array, (int(index) + 1) * (array.granularity + 1) - start_offset)


def _go_by_index_forward(array: Array, index: UDynamic, start_offset: int = 0) -> ToConvert:
    return _go_by_value_forward(array, (int(index) + 1) * (array.granularity + 1) - start_offset)


def _go_by_value_backward(array: Array, index: int) -> ToConvert:
    return inject(array, _create_sequence_left(index), array)


def _go_by_value_forward(array: Array, index: int) -> ToConvert:
    return inject(array, _create_sequence_right(index), array)


def _create_sequence_right(index: int) -> str:
    assert index >= 0
    return ">" * index


def _create_sequence_left(index: int) -> str:
    assert index >= 0
    return "<" * index

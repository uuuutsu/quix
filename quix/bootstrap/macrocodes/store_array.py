from quix.bootstrap.dtypes import Array
from quix.bootstrap.dtypes.const import DynamicUInt
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, inject


@convert
def store_array(array: Array, to_store: Wide | DynamicUInt, index: Wide | DynamicUInt) -> ToConvert:
    if isinstance(index, DynamicUInt):
        return _array_store_by_int(array, to_store, index)

    return None


def _array_store_by_int(array: Array, to_store: Wide | DynamicUInt, index: DynamicUInt) -> ToConvert:
    if isinstance(to_store, DynamicUInt):
        return _array_store_int_by_int(array, to_store, index)

    return None


def _array_store_int_by_int(array: Array, to_store: DynamicUInt, index: DynamicUInt) -> ToConvert:
    yield _go_by_index_forward(array, index)

    offset: int = 0
    for idx, value in enumerate(to_store, start=1):
        yield _go_by_value_forward(array, 1)
        yield add(array, value.value)

        if idx % array.granularity == 0:
            yield _go_by_value_forward(array, 1)
            offset += 1
        offset += 1

    yield _go_by_value_backward(array, offset)
    return _go_by_index_backward(array, index)


def _go_by_index_backward(array: Array, index: DynamicUInt) -> ToConvert:
    return _go_by_value_backward(array, (int(index) + 1) * (array.granularity + 1))


def _go_by_index_forward(array: Array, index: DynamicUInt) -> ToConvert:
    return _go_by_value_forward(array, (int(index) + 1) * (array.granularity + 1))


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

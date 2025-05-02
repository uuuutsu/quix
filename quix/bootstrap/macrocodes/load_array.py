from quix.bootstrap.dtypes import Array
from quix.bootstrap.dtypes.const import DynamicUInt
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, inject

from .clear_wide import clear_wide
from .store_array import _go_by_value, _move_in_array


@convert
def load_array(array: Array, load_in: Wide, index: Wide | DynamicUInt) -> ToConvert:
    yield clear_wide(load_in)

    if isinstance(index, DynamicUInt):
        return _array_load_by_int(array, load_in, index)

    return None


def _array_load_by_int(array: Array, load_in: Wide, index: DynamicUInt) -> ToConvert:
    offset: int = 1
    for unit in load_in:
        yield _array_load_unit_by_int(array, unit, index, offset)
        offset += 2 if offset % array.granularity == 0 else 1
    return None


def _array_load_unit_by_int(array: Array, unit: Unit, index: DynamicUInt, offset: int) -> ToConvert:
    return _array_load_unit_in_array(array, unit, (int(index) + 1) * (array.granularity + 1) + offset)


def _array_load_unit_in_array(array: Array, unit: Unit, offset: int) -> ToConvert:
    if offset == 0:
        buff, from_ = array.granularity + 1, offset
    else:
        buff, from_ = 0, offset

    yield _go_by_value(array, from_)
    yield inject(array, "[", array)
    yield add(array, -1)
    yield _go_by_value(array, buff - from_)
    yield add(array, 1)
    yield _go_by_value(array, -buff)
    yield add(unit, 1)
    yield _go_by_value(array, from_)
    yield inject(array, "]", array)
    yield _go_by_value(array, -from_)

    return _move_in_array(array, buff, from_)

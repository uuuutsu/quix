from quix.bootstrap.dtypes import Array
from quix.bootstrap.program import ToConvert, convert
from quix.memoptix import array


@convert
def init_array(value: Array) -> ToConvert:
    return array(value, value.full_length)

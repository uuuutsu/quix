from quix.bootstrap.dtypes import Array
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.memoptix import array


@macrocode
def init_array(value: Array) -> ToConvert:
    return array(value, value.full_length)

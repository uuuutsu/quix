from quix.bootstrap.dtypes import Str
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import output
from quix.memoptix.opcodes import free

from .add_unit import add_unit
from .clear_unit import clear_unit
from .sub_unit import sub_unit


@convert
def output_str(string: Str) -> ToConvert:
    buff = Unit("string_buff")

    last_val = 0
    for char in string:
        diff = ord(char) - last_val
        last_val = ord(char)

        if diff > 0:
            yield add_unit(buff, UInt8.from_value(abs(diff)), buff)
        else:
            yield sub_unit(buff, UInt8.from_value(abs(diff)), buff)

        yield output(buff)

    yield clear_unit(buff)
    return free(buff)

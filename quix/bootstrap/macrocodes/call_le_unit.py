from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocodes.call_ge_unit import call_ge_unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram


@convert
def call_le_unit(left: Unit, right: Unit, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    return call_ge_unit(right, left, if_, else_)

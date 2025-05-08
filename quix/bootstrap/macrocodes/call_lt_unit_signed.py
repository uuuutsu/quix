from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocodes.call_ge_unit_signed import call_ge_unit_signed
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram


@convert
def call_lt_unit_signed(left: Unit, right: Unit, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    return call_ge_unit_signed(left, right, else_, if_)

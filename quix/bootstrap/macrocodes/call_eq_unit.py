from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocodes.call_neq_unit import call_neq_unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram


@convert
def call_eq_unit(left: Unit, right: Unit, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    return call_neq_unit(left, right, else_, if_)

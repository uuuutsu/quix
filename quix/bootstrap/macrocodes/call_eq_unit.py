from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.call_neq_unit import call_neq_unit
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.base import CoreOpcode


@macrocode
def call_eq_unit(left: Unit, right: Unit, if_: CoreOpcode, else_: CoreOpcode) -> ToConvert:
    return call_neq_unit(left, right, else_, if_)

from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.call_neq_unit import call_neq_unit
from quix.bootstrap.program import ToConvert


@macrocode
def call_eq_unit(left: Unit, right: Unit, if_: ToConvert, else_: ToConvert) -> ToConvert:
    return call_neq_unit(left, right, else_, if_)

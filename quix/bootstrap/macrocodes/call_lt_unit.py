from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.call_ge_unit import call_ge_unit
from quix.bootstrap.program import ToConvert


@macrocode
def call_lt_unit(left: Unit, right: Unit, if_: ToConvert, else_: ToConvert) -> ToConvert:
    return call_ge_unit(left, right, else_, if_)

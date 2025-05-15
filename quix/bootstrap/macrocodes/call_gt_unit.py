from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.call_ge_unit import call_ge_unit
from quix.bootstrap.program import ToConvert


@macrocode
def call_gt_unit(left: Unit, right: Unit, if_: ToConvert, else_: ToConvert) -> ToConvert:
    return call_ge_unit(right, left, else_, if_)

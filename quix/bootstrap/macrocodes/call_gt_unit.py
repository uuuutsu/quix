from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.call_ge_unit import call_ge_unit
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.base import CoreOpcode


@macrocode
def call_gt_unit(left: Unit, right: Unit, if_: CoreOpcode, else_: CoreOpcode) -> ToConvert:
    return call_ge_unit(right, left, else_, if_)

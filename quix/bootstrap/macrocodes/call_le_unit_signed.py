from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.call_ge_unit_signed import call_ge_unit_signed
from quix.bootstrap.program import ToConvert


@macrocode
def call_le_unit_signed(left: Unit, right: Unit, if_: ToConvert, else_: ToConvert) -> ToConvert:
    return call_ge_unit_signed(right, left, if_, else_)

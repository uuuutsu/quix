from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.call_ge_unit_signed import call_ge_unit_signed
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.base import CoreOpcode


@macrocode
def call_le_unit_signed(left: Unit, right: Unit, if_: CoreOpcode, else_: CoreOpcode) -> ToConvert:
    return call_ge_unit_signed(right, left, if_, else_)

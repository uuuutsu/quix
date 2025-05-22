from quix.bootstrap.dtypes import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.base import CoreOpcode
from quix.tools import Arg, check

from .call_ge_wide_signed import call_ge_wide_signed


@macrocode
@check(Arg("left").size == Arg("right").size)
def call_le_wide_signed(left: Wide, right: Wide, if_: CoreOpcode, else_: CoreOpcode) -> ToConvert:
    return call_ge_wide_signed(right, left, if_, else_)

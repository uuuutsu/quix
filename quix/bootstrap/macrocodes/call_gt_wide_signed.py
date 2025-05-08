from quix.bootstrap.dtypes import Wide
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.tools import Arg, check

from .call_ge_wide_signed import call_ge_wide_signed


@convert
@check(Arg("left").size == Arg("right").size)
def call_gt_wide_signed(left: Wide, right: Wide, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    return call_ge_wide_signed(right, left, else_, if_)

from quix.bootstrap.dtypes import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.tools import Arg, check

from .call_ge_wide_signed import call_ge_wide_signed


@macrocode
@check(Arg("left").size == Arg("right").size)
def call_gt_wide_signed(left: Wide, right: Wide, if_: ToConvert, else_: ToConvert) -> ToConvert:
    return call_ge_wide_signed(right, left, else_, if_)

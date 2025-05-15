from quix.bootstrap.dtypes import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.tools import Arg, check

from .call_ge_wide import call_ge_wide


@macrocode
@check(Arg("left").size == Arg("right").size)
def call_lt_wide(left: Wide, right: Wide, if_: ToConvert, else_: ToConvert) -> ToConvert:
    return call_ge_wide(left, right, else_, if_)

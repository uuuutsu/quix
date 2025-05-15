from quix.bootstrap.dtypes import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.tools import Arg, check

from .call_neq_wide import call_neq_wide


@macrocode
@check(Arg("left").size == Arg("right").size)
def call_eq_wide(left: Wide, right: Wide, if_: ToConvert, else_: ToConvert) -> ToConvert:
    return call_neq_wide(left, right, else_, if_)

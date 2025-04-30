from quix.bootstrap.dtypes import Wide
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.tools import Arg, check

from .call_neq_wide import call_neq_wide


@convert
@check(Arg("left").size == Arg("right").size)
def call_eq_wide(left: Wide, right: Wide, if_: CoreProgram, else_: CoreProgram) -> ToConvert:
    return call_neq_wide(left, right, else_, if_)

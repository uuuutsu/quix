from quix.bootstrap.dtypes import Int8, UInt8, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, loop
from quix.memoptix.opcodes import free

from .add_unit import add_unit
from .assign_unit import assign_unit
from .clear_unit import clear_unit
from .copy_unit import copy_unit
from .move_unit import move_unit


@convert
def mul_unit(left: Unit | UInt8, right: Unit | UInt8, target: Unit) -> ToConvert:
    if isinstance(left, UInt8) and isinstance(right, UInt8):
        return assign_unit(target, left * right)
    elif isinstance(right, UInt8):
        return _mul_by_int(left, right, target)  # type: ignore
    elif isinstance(left, UInt8):
        return _mul_by_int(right, left, target)

    return _mul_two_units(left, right, target)


def _mul_by_int(
    left: Unit,
    right: UInt8,
    target: Unit,
) -> ToConvert:
    if left == target:
        return copy_unit(left, {target: (right - 1).to(Int8)})

    return clear_unit(target) | copy_unit(left, {target: right.to(Int8)})


def _mul_two_units(
    left: Unit,
    right: Unit,
    target: Unit,
) -> ToConvert:
    cand_buf, plier_buf = Unit("cand_buf"), Unit("plier_buf")

    if left == right:
        yield move_unit(left, {cand_buf: Int8.from_value(1), plier_buf: Int8.from_value(1)})
    else:
        yield move_unit(left, {cand_buf: Int8.from_value(1)})
        yield move_unit(right, {plier_buf: Int8.from_value(1)})

    yield clear_unit(target)

    loop_instrs = add_unit(cand_buf, target, target)
    if left != right != target:
        loop_instrs |= add(right, 1)
    loop_instrs |= add(plier_buf, -1)
    yield loop(plier_buf, loop_instrs)

    if left != target:
        yield move_unit(cand_buf, {left: Int8.from_value(1)})

    return [
        free(cand_buf),
        free(plier_buf),
    ]

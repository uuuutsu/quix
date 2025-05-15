from quix.bootstrap.dtypes import Cell, UCell, Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.opcodes import add, end_loop, start_loop
from quix.memoptix.opcodes import free

from .add_unit import add_unit
from .clear_unit import clear_unit
from .copy_unit import copy_unit
from .div_unit import div_unit
from .move_unit import move_unit
from .mul_unit import mul_unit


@macrocode
def or_unit(left: Unit, right: Unit, target: Unit) -> ToConvert:
    if left == right == target:
        return None
    if left == right:
        return clear_unit(target), copy_unit(left, {target: Cell.from_value(1)})

    lquot, rquot = Unit("lquot"), Unit("rquot")
    lrem, rrem = Unit("lrem"), Unit("rrem")
    bit_scale, break_ = Unit("bit_scale"), Unit("break_")
    ored_bit = Unit("ored_bit")

    yield copy_unit(left, {lquot: Cell.from_value(1)})
    yield copy_unit(right, {rquot: Cell.from_value(1)})
    yield add(break_, 8), add(bit_scale, 1), clear_unit(target)

    yield start_loop(break_)
    yield div_unit(lquot, UCell.from_value(2), lquot, lrem)
    yield div_unit(rquot, UCell.from_value(2), rquot, rrem)
    yield move_unit(lrem, {ored_bit: Cell.from_value(1)})
    yield move_unit(rrem, {ored_bit: Cell.from_value(1)})

    yield start_loop(ored_bit)
    yield add_unit(bit_scale, target, target)
    yield clear_unit(ored_bit)
    yield end_loop()

    yield add(break_, -1)
    yield mul_unit(bit_scale, UCell.from_value(2), bit_scale)
    return end_loop()

    yield clear_unit(bit_scale)

    return [
        free(ored_bit),
        free(lrem),
        free(rrem),
        free(bit_scale),
        free(lquot),
        free(rquot),
        free(break_),
    ]

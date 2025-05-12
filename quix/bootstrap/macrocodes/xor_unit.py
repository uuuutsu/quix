from quix.bootstrap.dtypes import Cell, UCell, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, end_loop, start_loop
from quix.memoptix.opcodes import free

from .add_unit import add_unit
from .call_z_unit import call_z_unit
from .clear_unit import clear_unit
from .copy_unit import copy_unit
from .div_unit import div_unit
from .move_unit import move_unit
from .mul_unit import mul_unit


@convert
def xor_unit(left: Unit, right: Unit, target: Unit) -> ToConvert:
    if left == right:
        return clear_unit(target)

    lquot, rquot = Unit("lquot"), Unit("rquot")
    lrem, rrem = Unit("lrem"), Unit("rrem")
    bit_scale, break_ = Unit("bit_scale"), Unit("break_")
    xored_bit = Unit("xored_bit")

    yield copy_unit(left, {lquot: Cell.from_value(1)})
    yield copy_unit(right, {rquot: Cell.from_value(1)})
    yield add(break_, 8), add(bit_scale, 1), clear_unit(target)

    yield start_loop(break_)
    yield div_unit(lquot, UCell.from_value(2), lquot, lrem)
    yield div_unit(rquot, UCell.from_value(2), rquot, rrem)
    yield move_unit(lrem, {xored_bit: Cell.from_value(1)})
    yield move_unit(rrem, {xored_bit: Cell.from_value(1)})
    yield start_loop(xored_bit)
    yield add(xored_bit, -1)
    yield call_z_unit(
        xored_bit,
        add_unit(target, bit_scale, target),
        clear_unit(xored_bit),
    )
    yield end_loop()
    yield add(break_, -1)
    yield mul_unit(bit_scale, UCell.from_value(2), bit_scale)
    yield end_loop()

    yield clear_unit(bit_scale)
    return [
        free(xored_bit),
        free(lrem),
        free(rrem),
        free(bit_scale),
        free(lquot),
        free(rquot),
        free(break_),
    ]

from quix.bootstrap.dtypes import Int8, UInt8, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, loop
from quix.memoptix.opcodes import free

from .add_unit import add_unit
from .clear_unit import clear_unit
from .copy_unit import copy_unit
from .div_unit import div_unit
from .move_unit import move_unit
from .mul_unit import mul_unit


@convert
def or_unit(left: Unit, right: Unit, target: Unit) -> ToConvert:
    if left == right == target:
        return None
    if left == right:
        return clear_unit(target), copy_unit(left, {target: Int8.from_value(1)})

    lquot, rquot = Unit("lquot"), Unit("rquot")
    lrem, rrem = Unit("lrem"), Unit("rrem")
    bit_scale, break_ = Unit("bit_scale"), Unit("break_")
    ored_bit = Unit("ored_bit")

    yield copy_unit(left, {lquot: Int8.from_value(1)})
    yield copy_unit(right, {rquot: Int8.from_value(1)})
    yield add(break_, 8), add(bit_scale, 1), clear_unit(target)

    instrs = div_unit(lquot, UInt8.from_value(2), lquot, lrem)
    instrs |= div_unit(rquot, UInt8.from_value(2), rquot, rrem)
    instrs |= move_unit(lrem, {ored_bit: Int8.from_value(1)}) | move_unit(rrem, {ored_bit: Int8.from_value(1)})
    instrs |= loop(ored_bit, add_unit(bit_scale, target, target) | clear_unit(ored_bit))
    instrs |= add(break_, -1)
    instrs |= mul_unit(bit_scale, UInt8.from_value(2), bit_scale)

    yield loop(break_, instrs)
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

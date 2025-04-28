from quix.bootstrap.dtypes import Int8, UInt8, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, loop
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

    yield copy_unit(left, {lquot: Int8.from_value(1)})
    yield copy_unit(right, {rquot: Int8.from_value(1)})
    yield add(break_, 8), add(bit_scale, 1), clear_unit(target)

    instrs = div_unit(lquot, UInt8.from_value(2), lquot, lrem)
    instrs |= div_unit(rquot, UInt8.from_value(2), rquot, rrem)
    instrs |= move_unit(lrem, {xored_bit: Int8.from_value(1)}) | move_unit(rrem, {xored_bit: Int8.from_value(1)})
    instrs |= loop(
        xored_bit,
        [
            add(xored_bit, -1),
            *call_z_unit(
                xored_bit,
                add_unit(target, bit_scale, target),
                clear_unit(xored_bit),
            ),
        ],
    )
    instrs |= add(break_, -1)
    instrs |= mul_unit(bit_scale, UInt8.from_value(2), bit_scale)

    yield loop(break_, instrs)
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

from quix.bootstrap.dtypes import Int8, UInt8, Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, end_loop, start_loop
from quix.memoptix.opcodes import free

from .add_unit import add_unit
from .clear_unit import clear_unit
from .copy_unit import copy_unit
from .div_unit import div_unit
from .mul_unit import mul_unit


@convert
def and_unit(left: Unit, right: Unit, target: Unit) -> ToConvert:
    if left == right == target:
        return None
    if left == right:
        return clear_unit(target), copy_unit(left, {target: Int8.from_value(1)})

    lquot, rquot = Unit("lquot"), Unit("rquot")
    lrem, rrem = Unit("lrem"), Unit("rrem")
    bit_scale, break_ = Unit("bit_scale"), Unit("break_")

    yield copy_unit(left, {lquot: Int8.from_value(1)})
    yield copy_unit(right, {rquot: Int8.from_value(1)})
    yield add(break_, 8), add(bit_scale, 1), clear_unit(target)

    yield start_loop(break_)
    yield div_unit(lquot, UInt8.from_value(2), lquot, lrem)
    yield div_unit(rquot, UInt8.from_value(2), rquot, rrem)

    yield start_loop(lrem)
    yield start_loop(rrem)
    yield add_unit(bit_scale, target, target) | add(rrem, -1)
    yield end_loop()
    yield add(lrem, -1)
    yield end_loop()

    yield add(break_, -1)
    yield mul_unit(bit_scale, UInt8.from_value(2), bit_scale)
    yield end_loop()

    yield clear_unit(lrem), clear_unit(rrem), clear_unit(bit_scale)
    return [
        free(lrem),
        free(rrem),
        free(bit_scale),
        free(lquot),
        free(rquot),
        free(break_),
    ]

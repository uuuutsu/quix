from logging import warning

from quix.bootstrap.dtypes import Wide
from quix.bootstrap.dtypes.const import Cell, UDynamic
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.tools import Arg, check

from .assign_wide import assign_wide
from .call_z_wide import call_z_wide
from .clear_wide import clear_wide
from .dec_wide import dec_wide
from .free_wide import free_wide
from .inc_wide import inc_wide
from .loop_wide import loop_wide
from .move_unit_carry import move_unit_carry


@macrocode
@check(Arg("left").size == Arg("right").size)
def div_wide(
    left: Wide | UDynamic,
    right: Wide | UDynamic,
    quotient: Wide | None,
    remainder: Wide | None,
) -> ToConvert:
    if remainder is quotient is None:
        return None
    elif remainder == quotient:
        raise ValueError("Remainder cannot be Quotient")

    if remainder and remainder.size < left.size:
        warning("Remainder of size smaller than division arguments may cause unexpected behaviour.")

    if isinstance(left, UDynamic) and isinstance(right, UDynamic):
        return _div_wide_ints(left, right, quotient, remainder)
    elif left == right:
        return _div_wide_by_itself(quotient, remainder)

    return _div_wides_and_ints(left, right, quotient, remainder)


def _div_wide_ints(
    left: UDynamic,
    right: UDynamic,
    quotient: Wide | None,
    remainder: Wide | None,
) -> ToConvert:
    quot_int, rem_int = divmod(left, right)

    if quotient:
        yield assign_wide(quotient, quot_int)

    if remainder:
        yield assign_wide(remainder, rem_int)

    return None


def _div_wide_by_itself(
    quotient: Wide | None,
    remainder: Wide | None,
) -> ToConvert:
    if quotient:
        yield assign_wide(quotient, UDynamic.from_int(0, size=quotient.size))

    if remainder:
        yield clear_wide(remainder)

    return None


def _div_wides_and_ints(
    left: Wide | UDynamic,
    right: Wide | UDynamic,
    quotient: Wide | None,
    remainder: Wide | None,
) -> ToConvert:
    rem_buff = Wide.from_length("rem_buff", right.size)
    left_buff = Wide.from_length("left_buff", left.size)

    dynamic_right: bool = False
    if isinstance(right, UDynamic):
        right_wide = Wide.from_length(f"{right.name}_buff", right.size)
        yield assign_wide(right_wide, right)
        dynamic_right = True
    elif right in [quotient, remainder]:
        right_wide = Wide.from_length(f"{right.name}_buff", right.size)
        yield _move_wide(right, {right_wide: Cell.from_value(1)})
        dynamic_right = True
    else:
        right_wide = right

    if isinstance(left, UDynamic):
        yield assign_wide(left_buff, left)
    else:
        yield _move_wide(left, {left_buff: Cell.from_value(1)})

    if quotient:
        yield clear_wide(quotient)

    def body() -> ToConvert:
        yield dec_wide(left_buff)
        yield dec_wide(right_wide)
        yield inc_wide(rem_buff)

        if (left not in (remainder, quotient)) and isinstance(left, Wide):
            yield inc_wide(left)

        def if_() -> ToConvert:
            yield _move_wide(rem_buff, {right_wide: Cell.from_value(1)})
            if quotient:
                yield inc_wide(quotient)
            return None

        return call_z_wide(right_wide, if_(), [])

    yield loop_wide(left_buff, body())
    yield free_wide(left_buff)

    if dynamic_right:
        yield clear_wide(right_wide), free_wide(right_wide)

    if remainder:
        yield clear_wide(remainder)
    if remainder and not dynamic_right:
        yield _move_wide(rem_buff, {right_wide: Cell.from_value(1), remainder: Cell.from_value(1)})
    elif remainder:
        yield _move_wide(rem_buff, {remainder: Cell.from_value(1)})
    elif not dynamic_right:
        yield _move_wide(rem_buff, {right_wide: Cell.from_value(1)})
    else:
        yield clear_wide(rem_buff)

    return free_wide(rem_buff)


@macrocode
def _move_wide(orig: Wide, to: dict[Wide, Cell]) -> ToConvert:
    for idx, unit in enumerate(orig):
        unit_target: dict[Unit, Cell] = {}
        carries: dict[Unit, tuple[Unit, ...]] = {}
        for target, scale in to.items():
            unit_target[target[idx]] = scale
            carries[target[idx]] = target[idx + 1 :]
        yield move_unit_carry(unit, unit_target, carries=carries)
    return None

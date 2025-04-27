from quix.bootstrap.dtypes import Int8, Unit
from quix.bootstrap.macrocodes import move_unit

from .utils import compile_to_bf


def test_move_unit_simple() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = move_unit(u1, {u2: Int8("scale", -1)}).builder()

    code = compile_to_bf(program, {u1: 0, u2: 1})
    assert code == "[->-<]"

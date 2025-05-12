from quix.bootstrap.dtypes import Cell, Unit
from quix.bootstrap.macrocodes import move_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_move_unit_simple() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 30),
        move_unit(u1, {u2: Cell.from_value(-2)}),
    )

    mem = run(program)

    assert mem[u1] == 0
    assert mem[u2] == 10  # 30 + (-2 * 10)

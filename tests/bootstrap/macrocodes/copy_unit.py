from quix.bootstrap.dtypes import Int8, Unit
from quix.bootstrap.macrocodes.copy_unit import copy_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_move_unit_simple() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 30),
        copy_unit(u1, {u2: Int8.from_value(-2)}),
    )

    mem = run(program)

    assert mem[u1] == 10
    assert mem[u2] == 10
    assert sum(mem.values()) == 20

from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import Int8
from quix.bootstrap.macrocodes import move_unit_carry
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_move_unit_carry_inc() -> None:
    u1, u2, u3 = Unit("u1"), Unit("u2"), Unit("u3")
    program = to_program(
        add(u1, 100),
        add(u2, 250),
        add(u3, 1),
        move_unit_carry(u1, {u2: Int8.from_value(1)}, {u2: (u3,)}),
    )

    mem = run(program)

    assert mem[u1] == 0
    assert mem[u2] == 94
    assert mem[u3] == 2
    assert sum(mem.values()) == 96


def test_move_unit_carry_dec() -> None:
    u1, u2, u3 = Unit("u1"), Unit("u2"), Unit("u3")
    program = to_program(
        add(u1, 2),
        add(u2, 1),
        add(u3, 0),
        move_unit_carry(u1, {u2: Int8.from_value(-1)}, {u2: (u3,)}),
    )

    mem = run(program)

    assert mem[u1] == 0
    assert mem[u2] == 255
    assert mem[u3] == 255
    assert sum(mem.values()) == 510

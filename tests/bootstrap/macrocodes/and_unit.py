from quix.bootstrap.dtypes import Unit
from quix.bootstrap.macrocodes.and_unit import and_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_and_unit() -> None:
    u1, u2, u3 = Unit("u1"), Unit("u2"), Unit("u3")
    program = to_program(
        add(u1, 10),
        add(u2, 12),
        add(u3, 2),
        and_unit(u1, u2, u3),
    )

    mem = run(program)

    assert mem[u1] == 10
    assert mem[u2] == 12
    assert mem[u3] == 8
    assert sum(mem.values()) == 30


def test_and_unit_same_left_target() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 12),
        and_unit(u1, u2, u1),
    )

    mem = run(program)

    assert mem[u2] == 12
    assert mem[u1] == 8
    assert sum(mem.values()) == 20


def test_and_unit_same_right_target() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 12),
        and_unit(u1, u2, u2),
    )

    mem = run(program)

    assert mem[u1] == 10
    assert sum(mem.values()) == 18


def test_and_unit_same_args() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 12),
        and_unit(u1, u1, u2),
    )

    mem = run(program)

    assert mem[u1] == 10
    assert mem[u2] == 10
    assert sum(mem.values()) == 20

from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.macrocodes import div_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_div_unit_rem() -> None:
    u1, u2, u3 = Unit("u1"), Unit("u2"), Unit("u3")
    program = to_program(
        add(u1, 57),
        add(u2, 13),
        add(u3, 2),
        div_unit(u1, u2, remainder=u3, quotient=None),
    )

    mem = run(program)

    assert mem[u1] == 57
    assert mem[u2] == 13
    assert mem[u3] == 5
    assert sum(mem.values()) == 75


def test_div_unit_quot() -> None:
    u1, u2, u3 = Unit("u1"), Unit("u2"), Unit("u3")
    program = to_program(
        add(u1, 57),
        add(u2, 13),
        add(u3, 2),
        div_unit(u1, u2, remainder=None, quotient=u3),
    )

    mem = run(program)

    assert mem[u1] == 57
    assert mem[u2] == 13
    assert mem[u3] == 4
    assert sum(mem.values()) == 74


def test_div_unit_rem_quot() -> None:
    u1, u2, u3, u4 = Unit("u1"), Unit("u2"), Unit("u3"), Unit("u4")
    program = to_program(
        add(u1, 57),
        add(u2, 13),
        add(u3, 2),
        div_unit(u1, u2, remainder=u3, quotient=u4),
    )

    mem = run(program)

    assert mem[u1] == 57
    assert mem[u2] == 13
    assert mem[u3] == 5
    assert mem[u4] == 4
    assert sum(mem.values()) == 79


def test_div_unit_same_rem() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 57),
        add(u2, 13),
        div_unit(u1, u2, remainder=u2, quotient=None),
    )

    mem = run(program)

    assert mem[u1] == 57
    assert mem[u2] == 5
    assert sum(mem.values()) == 62


def test_div_unit_same_quot() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 57),
        add(u2, 13),
        div_unit(u1, u2, remainder=None, quotient=u2),
    )

    mem = run(program)

    assert mem[u1] == 57
    assert mem[u2] == 4
    assert sum(mem.values()) == 61


def test_div_unit_same() -> None:
    u1 = Unit("u1")
    program = to_program(
        add(u1, 57),
        div_unit(u1, u1, remainder=None, quotient=u1),
    )

    mem = run(program)

    assert mem[u1] == 1
    assert sum(mem.values()) == 1


def test_div_unit_ints() -> None:
    u1 = Unit("u1")
    program = to_program(
        add(u1, 13),
        div_unit(UInt8.from_value(54), u1, remainder=None, quotient=u1),
    )

    mem = run(program)

    assert mem[u1] == 4
    assert sum(mem.values()) == 4

from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.macrocodes import sub_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_sub_unit_int() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        sub_unit(u1, UInt8.from_value(20), u2),
    )

    mem = run(program)

    assert mem[u1] == 10
    assert mem[u2] == 246
    assert sum(mem.values()) == 256


def test_sub_unit_unit() -> None:
    u1, u2, u3 = Unit("u1"), Unit("u2"), Unit("u3")
    program = to_program(
        add(u1, 50),
        add(u2, 30),
        add(u3, 5),
        sub_unit(u1, u2, u3),
    )

    mem = run(program)

    assert mem[u1] == 50
    assert mem[u2] == 30
    assert mem[u3] == 20
    assert sum(mem.values()) == 100


def test_sub_same_unit() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 5),
        sub_unit(u1, u1, u2),
    )

    mem = run(program)

    assert mem[u1] == 10
    assert mem[u2] == 0
    assert sum(mem.values()) == 10


def test_sub_same_unit_target() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 15),
        add(u2, 5),
        sub_unit(u1, u2, u1),
    )

    mem = run(program)

    assert mem[u1] == 10
    assert mem[u2] == 5
    assert sum(mem.values()) == 15


def test_sub_same_unit_everywhere() -> None:
    u1 = Unit("u1")
    program = to_program(
        add(u1, 10),
        sub_unit(u1, u1, u1),
    )

    mem = run(program)

    assert mem[u1] == 0
    assert sum(mem.values()) == 0

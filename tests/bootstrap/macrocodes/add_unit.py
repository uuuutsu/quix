from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.macrocodes import add_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_add_unit_int() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add_unit(u1, UInt8.from_value(20), u2),
    )

    mem = run(program)

    assert mem[u1] == 10
    assert mem[u2] == 30
    assert sum(mem.values()) == 40


def test_add_unit_unit() -> None:
    u1, u2, u3 = Unit("u1"), Unit("u2"), Unit("u3")
    program = to_program(
        add(u1, 10),
        add(u2, 30),
        add(u3, 5),
        add_unit(u1, u2, u3),
    )

    mem = run(program)

    assert mem[u1] == 10
    assert mem[u2] == 30
    assert mem[u3] == 40
    assert sum(mem.values()) == 80


def test_add_same_unit() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 5),
        add_unit(u1, u1, u2),
    )

    mem = run(program)

    assert mem[u1] == 10
    assert mem[u2] == 20
    assert sum(mem.values()) == 30


def test_add_same_unit_target_everywhere() -> None:
    u1 = Unit("u1")
    program = to_program(
        add(u1, 10),
        add_unit(u1, u1, u1),
    )

    mem = run(program)

    assert mem[u1] == 20
    assert sum(mem.values()) == 20

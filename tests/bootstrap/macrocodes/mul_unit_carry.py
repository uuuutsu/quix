from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.macrocodes import mul_unit_carry
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_mul_unit_carry_int() -> None:
    u1, u2, u3 = Unit("u1"), Unit("u2"), Unit("u3")
    program = to_program(
        add(u1, 10),
        mul_unit_carry(u1, UInt8.from_value(30), u2, (u3,)),
    )

    mem = run(program)

    assert mem[u1] == 10
    assert mem[u2] == 44
    assert mem[u3] == 1
    assert sum(mem.values()) == 55


def test_mul_unit_carry_unit() -> None:
    u1, u2, u3, u4 = Unit("u1"), Unit("u2"), Unit("u3"), Unit("u4")
    program = to_program(
        add(u1, 40),
        add(u2, 40),
        add(u3, 30),
        add(u4, -1),
        mul_unit_carry(u1, u2, u3, (u4,)),
    )

    mem = run(program)

    assert mem[u1] == 40
    assert mem[u2] == 40
    assert mem[u3] == 64
    assert mem[u4] == 5
    assert sum(mem.values()) == 149


def test_mul_unit_carry_same_unit() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 20),
        add(u2, 100),
        mul_unit_carry(u1, u1, u1, (u2,)),
    )

    mem = run(program)

    assert mem[u1] == 144
    assert mem[u2] == 101
    assert sum(mem.values()) == 245


def test_mul_unit_carry_two_ints() -> None:
    u1 = Unit("u1")
    program = to_program(
        add(u1, 100),
        mul_unit_carry(UInt8.from_value(20), UInt8.from_value(20), u1, (u1,)),
    )

    mem = run(program)

    assert mem[u1] == 145
    assert sum(mem.values()) == 145

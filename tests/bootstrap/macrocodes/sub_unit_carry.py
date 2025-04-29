from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.macrocodes import sub_unit_carry
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_sub_unit_carry_int() -> None:
    u1, u2, u3 = Unit("u1"), Unit("u2"), Unit("u3")
    program = to_program(
        add(u1, 100),
        sub_unit_carry(u1, UInt8.from_value(250), u2, (u3,)),
    )

    mem = run(program)

    assert mem[u1] == 100
    assert mem[u2] == 106
    assert mem[u3] == 255
    assert sum(mem.values()) == 461


def test_sub_unit_carry_int_no_carry() -> None:
    u1, u2, u3 = Unit("u1"), Unit("u2"), Unit("u3")
    program = to_program(
        add(u1, 100),
        sub_unit_carry(u1, UInt8.from_value(100), u2, (u3,)),
    )

    mem = run(program)

    assert mem[u1] == 100
    assert mem[u2] == 0
    assert mem[u3] == 0
    assert sum(mem.values()) == 100


def test_sub_unit_carry_unit() -> None:
    u1, u2, u3, u4 = Unit("u1"), Unit("u2"), Unit("u3"), Unit("u4")
    program = to_program(
        add(u1, 100),
        add(u2, 250),
        add(u3, 255),
        add(u4, -1),
        sub_unit_carry(u1, u2, u3, (u4,)),
    )

    mem = run(program)

    assert mem[u1] == 100
    assert mem[u2] == 250
    assert mem[u3] == 106
    assert mem[u4] == 254
    assert sum(mem.values()) == 710


def test_sub_unit_carry_same_unit() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 100),
        add(u2, 250),
        sub_unit_carry(u1, u1, u1, (u2,)),
    )

    mem = run(program)

    assert mem[u1] == 0
    assert mem[u2] == 250
    assert sum(mem.values()) == 250

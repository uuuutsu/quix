from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.macrocodes import add_unit_carry
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_add_unit_carry_int() -> None:
    u1, u2, u3 = Unit("u1"), Unit("u2"), Unit("u3")
    program = to_program(
        add(u1, 100),
        add_unit_carry(u1, UInt8.from_value(250), u2, (u3,)),
    )

    mem = run(program)

    assert mem[u1] == 100
    assert mem[u2] == 94
    assert mem[u3] == 1
    assert sum(mem.values()) == 195


def test_add_unit_carry_unit() -> None:
    u1, u2, u3, u4 = Unit("u1"), Unit("u2"), Unit("u3"), Unit("u4")
    program = to_program(
        add(u1, 100),
        add(u2, 250),
        add(u3, 255),
        add(u4, -1),
        add_unit_carry(u1, u2, u3, (u4,)),
    )

    mem = run(program)

    assert mem[u1] == 100
    assert mem[u2] == 250
    assert mem[u3] == 94
    assert mem[u4] == 0
    assert sum(mem.values()) == 444

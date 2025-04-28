from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.macrocodes import not_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_not_unit_int() -> None:
    u1 = Unit("u1")
    program = to_program(
        add(u1, 10),
        not_unit(UInt8.from_value(13), u1),
    )

    mem = run(program)

    assert mem[u1] == 242
    assert sum(mem.values()) == 242


def test_not_unit() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 13),
        not_unit(u2, u1),
    )

    mem = run(program)

    assert mem[u1] == 242
    assert mem[u2] == 13
    assert sum(mem.values()) == 255


def test_not_unit_same() -> None:
    u1 = Unit("u1")
    program = to_program(
        add(u1, 47),
        not_unit(u1, u1),
        not_unit(u1, u1),
    )

    mem = run(program)

    assert mem[u1] == 47
    assert sum(mem.values()) == 47

from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocodes import switch_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_switch_unit() -> None:
    u1 = Unit("u1")
    program = to_program(
        add(u1, 3),
        switch_unit(
            u1,
            {
                UInt8.from_value(1): [add(u1, 5)],
                UInt8.from_value(3): [add(u1, 13)],
                UInt8.from_value(5): [add(u1, 27)],
            },
        ),
    )

    mem = run(program)
    assert mem[u1] == 16
    assert sum(mem.values()) == 16


def test_switch_unit_none() -> None:
    u1 = Unit("u1")
    program = to_program(
        add(u1, 4),
        switch_unit(
            u1,
            {
                UInt8.from_value(1): [add(u1, 5)],
                UInt8.from_value(3): [add(u1, 13)],
                UInt8.from_value(5): [add(u1, 27)],
            },
        ),
    )

    mem = run(program)
    assert mem[u1] == 4
    assert sum(mem.values()) == 4

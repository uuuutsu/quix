from quix.bootstrap.dtypes.const import UCell
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocodes import switch_unit
from quix.bootstrap.macrocodes.nop import NOP
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
                UCell.from_value(1): add(u1, 5),
                UCell.from_value(3): add(u1, 13),
                UCell.from_value(5): add(u1, 27),
            },
            NOP,
        ),
    )

    mem = run(program)
    assert mem[u1] == 16
    assert sum(mem.values()) == 16


def test_switch_unit_else() -> None:
    u1 = Unit("u1")
    program = to_program(
        add(u1, 4),
        switch_unit(
            u1,
            {
                UCell.from_value(1): add(u1, 5),
                UCell.from_value(3): add(u1, 13),
                UCell.from_value(5): add(u1, 27),
            },
            add(u1, -4),
        ),
    )

    mem = run(program)
    assert mem[u1] == 0
    assert sum(mem.values()) == 0

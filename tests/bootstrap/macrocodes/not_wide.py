from quix.bootstrap.dtypes import UCell, UDynamic, Wide
from quix.bootstrap.macrocodes import not_wide
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_not_wide_int() -> None:
    w1 = Wide.from_length("w1", 2)
    program = to_program(
        add(w1[0], 10),
        add(w1[1], 20),
        not_wide(UDynamic.from_value((UCell.from_value(5), UCell.from_value(15))), w1),
    )

    mem = run(program)

    assert mem[w1[0]] == 250
    assert mem[w1[1]] == 240
    assert sum(mem.values()) == 490

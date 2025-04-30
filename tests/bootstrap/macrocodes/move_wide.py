from quix.bootstrap.dtypes import Int8, Wide
from quix.bootstrap.dtypes.const import DynamicInt
from quix.bootstrap.macrocodes import move_wide
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_move_wide_simple() -> None:
    w1, w2 = Wide.from_length("w1", 2), Wide.from_length("w2", 2)
    program = to_program(
        add(w1[0], 20),
        add(w1[1], 40),
        add(w2[0], 200),
        add(w2[1], 150),
        move_wide(w1, {w2: DynamicInt.from_value((Int8.from_value(-3), Int8.from_value(-2)))}),
    )

    mem = run(program)

    assert mem[w1[0]] == 0
    assert mem[w1[1]] == 0

    assert mem[w2[0]] == 140
    assert mem[w2[1]] == 70

    assert sum(mem.values()) == 210

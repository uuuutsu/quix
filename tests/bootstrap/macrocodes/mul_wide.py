from quix.bootstrap.dtypes import Wide
from quix.bootstrap.macrocodes import mul_wide
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_mul_wide_wides() -> None:
    w1, w2, w3 = Wide.from_length("w1", 2), Wide.from_length("w2", 2), Wide.from_length("w3", 2)

    program = to_program(
        add(w1[0], 10),
        add(w2[1], 20),
        mul_wide(w1, w2, w3),
    )

    mem = run(program)

    assert mem[w1[0]] == 10
    assert mem[w1[1]] == 0

    assert mem[w2[0]] == 0
    assert mem[w2[1]] == 20

    assert mem[w3[0]] == 0
    assert mem[w3[1]] == 0

    assert sum(mem.values()) == 30


def test_mul_wide_same_wide() -> None:
    w1 = Wide.from_length("w1", 2)

    program = to_program(
        add(w1[0], 20),
        add(w1[1], 10),
        mul_wide(w1, w1, w1),
    )

    mem = run(program)

    assert mem[w1[0]] == 144
    assert mem[w1[1]] == 101

    assert sum(mem.values()) == 245

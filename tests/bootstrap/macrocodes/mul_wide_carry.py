from quix.bootstrap.dtypes import Unit, Wide
from quix.bootstrap.macrocodes import mul_wide_carry
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_mul_wide_carry_wides() -> None:
    w1, w2, w3 = Wide.from_length("w1", 2), Wide.from_length("w2", 2), Wide.from_length("w3", 2)
    c1 = Unit("c1")
    program = to_program(
        add(w1[0], 0),
        add(w1[1], 10),
        add(w2[0], 10),
        add(w2[1], 110),
        add(w3[1], 255),
        add(c1, 1),
        mul_wide_carry(w1, w2, w3, (c1,)),
    )

    mem = run(program)

    assert mem[w1[0]] == 0
    assert mem[w1[1]] == 10

    assert mem[w2[0]] == 10
    assert mem[w2[1]] == 110

    assert mem[w3[0]] == 0
    assert mem[w3[1]] == 76

    assert mem[c1] == 5

    assert sum(mem.values()) == 211

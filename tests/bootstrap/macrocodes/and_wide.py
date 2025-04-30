from quix.bootstrap.dtypes import Wide
from quix.bootstrap.macrocodes import and_wide
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_and_wide_wides() -> None:
    w1, w2, w3 = Wide.from_length("w1", 2), Wide.from_length("w2", 2), Wide.from_length("w3", 2)

    program = to_program(
        add(w1[0], 154),
        add(w1[1], 219),
        add(w2[0], 19),
        add(w2[1], 187),
        add(w3[0], 10),
        and_wide(w1, w2, w3),
    )

    mem = run(program)

    assert mem[w1[0]] == 154
    assert mem[w1[1]] == 219

    assert mem[w2[0]] == 19
    assert mem[w2[1]] == 187

    assert mem[w3[0]] == 18
    assert mem[w3[1]] == 155

    assert sum(mem.values()) == 752

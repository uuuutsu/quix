from quix.bootstrap.dtypes import Wide
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocodes import call_le_wide
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_call_le_wide_if() -> None:
    w1, w2 = Wide.from_length("w1", 2), Wide.from_length("w2", 2)
    u1 = Unit("u1")
    program = to_program(
        add(w1[0], 250),
        add(w1[1], 150),
        add(w2[0], 250),
        add(w2[1], 150),
        call_le_wide(
            w1,
            w2,
            [
                add(u1, 1),
            ],
            [
                add(u1, 2),
            ],
        ),
    )

    mem = run(program)

    assert mem[w1[0]] == 250
    assert mem[w1[1]] == 150

    assert mem[w2[0]] == 250
    assert mem[w2[1]] == 150

    assert mem[u1] == 1

    assert sum(mem.values()) == 801

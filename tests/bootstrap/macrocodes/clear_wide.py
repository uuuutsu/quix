from quix.bootstrap.dtypes import Wide
from quix.bootstrap.macrocodes import clear_wide
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_clear_wide() -> None:
    w1 = Wide.from_length("w1", 2)

    program = to_program(
        add(w1[0], 10),
        add(w1[1], 50),
        clear_wide(w1),
    )
    mem = run(program)

    assert mem[w1[0]] == 0
    assert mem[w1[1]] == 0
    assert sum(mem.values()) == 0

from quix.bootstrap.dtypes import Unit, Wide
from quix.bootstrap.macrocodes import clear_wide
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_clear_wide_simple() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    w1 = Wide("wide", (u1, u2))
    program = to_program(add(u1, 10), add(u2, 10), clear_wide(w1))

    mem = run(program)

    assert mem[u1] == 0
    assert mem[u2] == 0

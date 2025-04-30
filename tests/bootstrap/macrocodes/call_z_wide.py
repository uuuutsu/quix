from quix.bootstrap.dtypes import Unit, Wide
from quix.bootstrap.macrocodes import call_z_wide
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_call_z_wide_else() -> None:
    w1, u2 = Wide.from_length("u1", 10), Unit("u2")
    program = to_program(
        add(u2, 10),
        add(w1[1], 1),
        call_z_wide(
            w1,
            [
                add(u2, 1),
            ],
            [
                add(u2, 2),
            ],
        ),
    )

    mem = run(program)

    assert mem[w1[0]] == 0
    assert mem[w1[1]] == 1

    assert mem[u2] == 12

    assert sum(mem.values()) == 13


def test_call_z_wide_if() -> None:
    w1, u2 = Wide.from_length("u1", 10), Unit("u2")
    program = to_program(
        add(u2, 10),
        call_z_wide(
            w1,
            [
                add(u2, 1),
            ],
            [
                add(u2, 2),
            ],
        ),
    )

    mem = run(program)

    assert mem[w1[0]] == 0
    assert mem[w1[1]] == 0

    assert mem[u2] == 11

    assert sum(mem.values()) == 11

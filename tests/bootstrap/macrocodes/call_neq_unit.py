from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocodes import call_neq_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_call_neq_unit_else() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 15),
        add(u2, 15),
        call_neq_unit(
            u1,
            u2,
            [
                add(u2, 1),
            ],
            [
                add(u2, 2),
            ],
        ),
    )

    mem = run(program)

    assert mem[u1] == 15
    assert mem[u2] == 17
    assert sum(mem.values()) == 32


def test_call_neq_unit_if() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 11),
        call_neq_unit(
            u1,
            u2,
            [
                add(u2, -1),
            ],
            [
                add(u1, 2),
            ],
        ),
    )

    mem = run(program)
    assert mem[u1] == 10
    assert mem[u2] == 10
    assert sum(mem.values()) == 20


def test_call_neq_unit_if_if() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 35),
        call_neq_unit(
            u2,
            u1,
            [
                add(u1, 26),
                *call_neq_unit(
                    u1,
                    u2,
                    [
                        add(u2, 10),
                        add(u1, 4),
                    ],
                    [
                        add(u2, 5),
                    ],
                ),
            ],
            [
                add(u2, 2),
            ],
        ),
    )

    mem = run(program)
    assert mem[u1] == 40
    assert mem[u2] == 45
    assert sum(mem.values()) == 85


def test_call_neq_unit_if_else() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 34),
        add(u2, 35),
        call_neq_unit(
            u1,
            u2,
            [
                add(u1, 1),
                *call_neq_unit(
                    u2,
                    u1,
                    [
                        add(u2, 10),
                        add(u1, 4),
                    ],
                    [
                        add(u2, 5),
                        add(u1, -1),
                    ],
                ),
                add(u1, -10),
            ],
            [
                add(u2, 2),
            ],
        ),
    )

    mem = run(program)
    assert mem[u1] == 24
    assert mem[u2] == 40
    assert sum(mem.values()) == 64


def test_call_neq_unit_else_if() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        call_neq_unit(
            u1,
            u2,
            [
                add(u1, 1),
                add(u2, -1),
            ],
            [
                add(u1, -2),
                add(u2, 1),
                *call_neq_unit(
                    u1,
                    u2,
                    [
                        add(u2, 10),
                        add(u1, 4),
                    ],
                    [
                        add(u2, 3),
                        add(u1, -1),
                    ],
                ),
                add(u1, 5),
            ],
        ),
    )

    mem = run(program)

    assert mem[u1] == 7
    assert mem[u2] == 11
    assert sum(mem.values()) == 18


def test_call_neq_unit_else_else() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 1),
        add(u2, 1),
        call_neq_unit(
            u1,
            u2,
            [
                add(u2, -1),
            ],
            [
                add(u1, 2),
                add(u2, 2),
                *call_neq_unit(
                    u2,
                    u2,
                    [
                        add(u2, 10),
                        add(u1, 4),
                    ],
                    [
                        add(u2, 3),
                        add(u1, -1),
                    ],
                ),
                add(u1, 5),
            ],
        ),
    )

    mem = run(program)
    assert mem[u1] == 7
    assert mem[u2] == 6
    assert sum(mem.values()) == 13

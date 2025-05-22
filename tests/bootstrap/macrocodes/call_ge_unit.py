from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import call_ge_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_call_ge_unit_else() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 14),
        add(u2, 15),
        call_ge_unit(
            u1,
            u2,
            add(u2, 1),
            add(u2, 2),
        ),
    )

    mem = run(program)

    assert mem[u1] == 14
    assert mem[u2] == 17
    assert sum(mem.values()) == 31


def test_call_ge_unit_if_greater() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 36),
        add(u2, 35),
        call_ge_unit(
            u1,
            u2,
            add(u2, -1),
            add(u1, 2),
        ),
    )

    mem = run(program)
    assert mem[u1] == 36
    assert mem[u2] == 34
    assert sum(mem.values()) == 70


def test_call_ge_unit_if_equal() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 35),
        add(u2, 35),
        call_ge_unit(
            u1,
            u2,
            add(u2, -1),
            add(u1, 2),
        ),
    )

    mem = run(program)
    assert mem[u1] == 35
    assert mem[u2] == 34
    assert sum(mem.values()) == 69


def test_call_ge_unit_if_if() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 35),
        call_ge_unit(
            u2,
            u1,
            macrocode(
                add(u1, 25),
                call_ge_unit(
                    u1,
                    u2,
                    macrocode(
                        add(u2, 10),
                        add(u1, 4),
                    ),
                    add(u2, 5),
                ),
            ),
            add(u2, 2),
        ),
    )

    mem = run(program)
    assert mem[u1] == 39
    assert mem[u2] == 45
    assert sum(mem.values()) == 84


def test_call_ge_unit_if_else() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 34),
        add(u2, 30),
        call_ge_unit(
            u1,
            u2,
            macrocode(
                add(u1, -5),
                call_ge_unit(
                    u1,
                    u2,
                    macrocode(
                        add(u2, 10),
                        add(u1, 4),
                    ),
                    macrocode(
                        add(u2, 5),
                        add(u1, -1),
                    ),
                ),
                add(u1, -10),
            ),
            add(u2, 2),
        ),
    )

    mem = run(program)
    assert mem[u1] == 18
    assert mem[u2] == 35
    assert sum(mem.values()) == 53


def test_call_ge_unit_else_if() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u2, -1),
        call_ge_unit(
            u1,
            u2,
            macrocode(
                add(u1, 1),
                add(u2, -1),
            ),
            macrocode(
                add(u1, -2),
                add(u2, 1),
                call_ge_unit(
                    u1,
                    u2,
                    macrocode(
                        add(u2, 10),
                        add(u1, 4),
                    ),
                    macrocode(
                        add(u2, 3),
                        add(u1, -1),
                    ),
                ),
                add(u1, 5),
            ),
        ),
    )

    mem = run(program)

    assert mem[u1] == 7
    assert mem[u2] == 10
    assert sum(mem.values()) == 17


def test_call_ge_unit_else_else() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u2, 1),
        call_ge_unit(
            u1,
            u2,
            add(u2, -1),
            macrocode(
                add(u1, 3),
                add(u2, 1),
                call_ge_unit(
                    u2,
                    u1,
                    macrocode(
                        add(u2, 10),
                        add(u1, 4),
                    ),
                    macrocode(
                        add(u2, 3),
                        add(u1, -1),
                    ),
                ),
                add(u1, 5),
            ),
        ),
    )

    mem = run(program)
    assert mem[u1] == 7
    assert mem[u2] == 5
    assert sum(mem.values()) == 12

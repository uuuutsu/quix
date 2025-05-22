from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import call_ge_unit_signed
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_call_ge_unit_signed_else() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 129),
        add(u2, 15),
        call_ge_unit_signed(
            u1,
            u2,
            add(u2, 1),
            add(u2, 2),
        ),
    )

    mem = run(program)

    assert mem[u1] == 129
    assert mem[u2] == 17
    assert sum(mem.values()) == 146


def test_call_ge_unit_signed_if_greater() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 131),
        add(u2, 130),
        call_ge_unit_signed(
            u1,
            u2,
            add(u2, -1),
            add(u1, 2),
        ),
    )

    mem = run(program)
    assert mem[u1] == 131
    assert mem[u2] == 129
    assert sum(mem.values()) == 260


def test_call_ge_unit_signed_if_equal() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 35),
        add(u2, 35),
        call_ge_unit_signed(
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


def test_call_ge_unit_signed_if_if() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 10),
        add(u2, 35),
        call_ge_unit_signed(
            u2,
            u1,
            macrocode(
                add(u1, 125),
                call_ge_unit_signed(
                    u2,
                    u1,
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
    assert mem[u1] == 139
    assert mem[u2] == 45
    assert sum(mem.values()) == 184

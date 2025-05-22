from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocode import from_program
from quix.bootstrap.macrocodes import call_z_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_call_z_unit_else() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 1),
        call_z_unit(
            u1,
            add(u2, 1),
            add(u2, 2),
        ),
        add(u2, -2),
    )

    mem = run(program)
    assert mem[u1] == 1
    assert mem[u2] == 0
    assert sum(mem.values()) == 1


def test_call_z_unit_if() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        call_z_unit(
            u1,
            add(u2, 1),
            add(u2, 2),
        ),
    )

    mem = run(program)
    assert mem[u1] == 0
    assert mem[u2] == 1
    assert sum(mem.values()) == 1


def test_call_z_unit_if_if() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        call_z_unit(
            u1,
            from_program(
                add(u2, 1),
                call_z_unit(
                    u1,
                    from_program(
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
    assert mem[u1] == 4
    assert mem[u2] == 11
    assert sum(mem.values()) == 15


def test_call_z_unit_if_else() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        call_z_unit(
            u1,
            from_program(
                add(u2, 1),
                add(u1, 1),
                call_z_unit(
                    u1,
                    from_program(
                        add(u2, 10),
                        add(u1, 4),
                    ),
                    from_program(
                        add(u2, 5),
                        add(u1, -1),
                    ),
                ),
            ),
            add(u2, 2),
        ),
    )

    mem = run(program)
    assert mem[u1] == 0
    assert mem[u2] == 6
    assert sum(mem.values()) == 6


def test_call_z_unit_else_if() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 1),
        call_z_unit(
            u1,
            add(u2, -1),
            from_program(
                add(u1, -1),
                call_z_unit(
                    u1,
                    from_program(
                        add(u2, 10),
                        add(u1, 4),
                    ),
                    from_program(
                        add(u2, 3),
                        add(u1, -1),
                    ),
                ),
                add(u1, 5),
            ),
        ),
    )

    mem = run(program)
    assert mem[u1] == 9
    assert mem[u2] == 10
    assert sum(mem.values()) == 19


def test_call_z_unit_else_else() -> None:
    u1, u2 = Unit("u1"), Unit("u2")
    program = to_program(
        add(u1, 1),
        call_z_unit(
            u1,
            add(u2, -1),
            from_program(
                add(u1, 2),
                call_z_unit(
                    u1,
                    from_program(
                        add(u2, 10),
                        add(u1, 4),
                    ),
                    from_program(
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
    assert mem[u2] == 3
    assert sum(mem.values()) == 10

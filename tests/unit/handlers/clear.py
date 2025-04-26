from quix.core.opcodes.opcodes import inject
from quix.unit.handlers import clear
from quix.unit.opcodes import unit


def test_clear_wide() -> None:
    u1, u2 = unit("u1"), unit("u2")

    assert set(clear([u1, u2]).program) == {
        inject(u1, "[-]", u1, True),
        inject(u2, "[-]", u2, True),
    }

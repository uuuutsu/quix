from quix.core.opcodes.opcodes import inject
from quix.unit.handlers import clear
from quix.unit.opcodes import unit


def test_clear_wide() -> None:
    u1, u2 = unit("u1"), unit("u2")

    assert clear([u1, u2]).program == [
        inject(u1.ref, "[-]", u1.ref, True),
        inject(u2.ref, "[-]", u2.ref, True),
    ] or clear([u1, u2]).program == [
        inject(u2.ref, "[-]", u2.ref, True),
        inject(u1.ref, "[-]", u1.ref, True),
    ]

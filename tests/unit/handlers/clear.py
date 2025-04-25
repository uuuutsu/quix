from quix.core.opcodes.opcodes import inject
from quix.unit.handlers import clear
from quix.unit.opcodes import unit


def test_clear_unit() -> None:
    u1 = unit("u1")
    assert clear(u1).program == [inject(u1.ref, "[-]", u1.ref)]  # type: ignore


def test_clear_wide() -> None:
    u1, u2 = unit("u1"), unit("u2")

    assert clear([u1, u2]).program == [  # type: ignore
        inject(u1.ref, "[-]", u1.ref),
        inject(u2.ref, "[-]", u2.ref),
    ] or clear([u1, u2]).program == [  # type: ignore
        inject(u2.ref, "[-]", u2.ref),
        inject(u1.ref, "[-]", u1.ref),
    ]

from quix.bootstrap.dtypes import Wide
from quix.bootstrap.dtypes.const import UCell, UDynamic
from quix.bootstrap.macrocodes import sub_wide
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_sub_wide_wides() -> None:
    w1, w2, w3 = Wide.from_length("w1", 2), Wide.from_length("w2", 2), Wide.from_length("w3", 2)

    program = to_program(
        add(w1[0], 10),
        add(w2[0], 20),
        add(w2[1], 20),
        sub_wide(w1, w2, w3),
    )

    mem = run(program)

    assert mem[w1[0]] == 10
    assert mem[w1[1]] == 0

    assert mem[w2[0]] == 20
    assert mem[w2[1]] == 20

    assert mem[w3[0]] == 246
    assert mem[w3[1]] == 235

    assert sum(mem.values()) == 531


def test_sub_wide_same_wide() -> None:
    w1 = Wide.from_length("w1", 2)

    program = to_program(
        add(w1[0], 10),
        add(w1[1], 20),
        sub_wide(w1, w1, w1),
    )

    mem = run(program)

    assert mem[w1[0]] == 0
    assert mem[w1[1]] == 0

    assert sum(mem.values()) == 0


def test_sub_wide_overflow() -> None:
    w1, w2, w3 = Wide.from_length("w1", 2), Wide.from_length("w2", 2), Wide.from_length("w3", 2)

    program = to_program(
        add(w1[0], 150),
        add(w1[1], 250),
        add(w2[0], 151),
        add(w2[1], 255),
        sub_wide(w1, w2, w3),
    )

    mem = run(program)

    assert mem[w1[0]] == 150
    assert mem[w1[1]] == 250

    assert mem[w2[0]] == 151
    assert mem[w2[1]] == 255

    assert mem[w3[0]] == 255
    assert mem[w3[1]] == 250

    assert sum(mem.values()) == 1311


def test_sub_wide_ints() -> None:
    w1, w2 = Wide.from_length("w1", 2), Wide.from_length("w2", 2)

    program = to_program(
        add(w1[0], 106),
        add(w1[1], 49),
        add(w2[1], 5),
        sub_wide(
            w1,
            UDynamic.from_value(
                (
                    UCell.from_value(106),
                    UCell.from_value(50),
                )
            ),
            w2,
        ),
    )

    mem = run(program)

    assert mem[w1[0]] == 106
    assert mem[w1[1]] == 49

    assert mem[w2[0]] == 0
    assert mem[w2[1]] == 255

    assert sum(mem.values()) == 410

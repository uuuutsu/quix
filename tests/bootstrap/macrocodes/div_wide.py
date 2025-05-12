from quix.bootstrap.dtypes import Wide
from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.macrocodes import div_wide
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_div_wide_rem() -> None:
    w1, w2, w3 = Wide.from_length("w1", 2), Wide.from_length("w2", 2), Wide.from_length("w3", 2)

    program = to_program(
        add(w1[0], 137),
        add(w1[1], 55),
        add(w2[0], 34),
        add(w2[1], 12),
        add(w3[0], 12),
        div_wide(w1, w2, remainder=w3, quotient=None),
    )

    mem = run(program)

    assert mem[w1[0]] == 137
    assert mem[w1[1]] == 55

    assert mem[w2[0]] == 34
    assert mem[w2[1]] == 12

    assert mem[w3[0]] == 1
    assert mem[w3[1]] == 7

    assert sum(mem.values()) == 246


def test_div_wide_quot() -> None:
    w1, w2, w3 = Wide.from_length("w1", 2), Wide.from_length("w2", 2), Wide.from_length("w3", 2)

    program = to_program(
        add(w1[0], 137),
        add(w1[1], 55),
        add(w2[0], 34),
        add(w2[1], 12),
        add(w3[0], 12),
        div_wide(w1, w2, remainder=None, quotient=w3),
    )

    mem = run(program)

    assert mem[w1[0]] == 137
    assert mem[w1[1]] == 55

    assert mem[w2[0]] == 34
    assert mem[w2[1]] == 12

    assert mem[w3[0]] == 4
    assert mem[w3[1]] == 0

    assert sum(mem.values()) == 242


def test_div_wide_rem_quot() -> None:
    w1, w2, w3, w4 = (
        Wide.from_length("w1", 2),
        Wide.from_length("w2", 2),
        Wide.from_length("w3", 2),
        Wide.from_length("w4", 2),
    )

    program = to_program(
        add(w1[0], 137),
        add(w1[1], 55),
        add(w2[0], 34),
        add(w2[1], 12),
        add(w3[0], 12),
        div_wide(w1, w2, remainder=w3, quotient=w4),
    )

    mem = run(program)

    assert mem[w1[0]] == 137
    assert mem[w1[1]] == 55

    assert mem[w2[0]] == 34
    assert mem[w2[1]] == 12

    assert mem[w3[0]] == 1
    assert mem[w3[1]] == 7

    assert mem[w4[0]] == 4
    assert mem[w4[1]] == 0

    assert sum(mem.values()) == 250


def test_div_wide_by_int() -> None:
    w1, w3, w4 = (
        Wide.from_length("w1", 2),
        Wide.from_length("w3", 2),
        Wide.from_length("w4", 2),
    )

    program = to_program(
        add(w1[0], 137),
        add(w1[1], 55),
        add(w3[0], 12),
        div_wide(w1, UDynamic.from_int(716, 2), remainder=w3, quotient=w4),
    )

    mem = run(program)

    assert mem[w1[0]] == 137
    assert mem[w1[1]] == 55

    assert mem[w3[0]] == 101
    assert mem[w3[1]] == 2

    assert mem[w4[0]] == 19
    assert mem[w4[1]] == 0

    assert sum(mem.values()) == 314

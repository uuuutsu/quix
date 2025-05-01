from quix.bootstrap.dtypes import Array, DynamicUInt, Unit, Wide
from quix.bootstrap.macrocodes import init_array, store_array
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run_with_tape


def test_store_array_int_by_int() -> None:
    a1, u1 = Array("a1", length=10), Unit("u1")
    program = to_program(
        init_array(a1),
        store_array(a1, DynamicUInt.from_int(257, 2), DynamicUInt.from_int(5)),
        add(u1, 5),
    )

    indexes, tape = run_with_tape(program)

    assert tape[indexes[a1] + 13] == 1
    assert tape[indexes[a1] + 15] == 1
    assert tape[indexes[u1]] == 5

    assert sum(tape) == 7


def test_store_array_wide_by_int() -> None:
    w1 = Wide.from_length("w1", 2)
    a1, u1 = Array("a1", length=10), Unit("u1")
    program = to_program(
        add(w1[0], 100),
        add(w1[1], 70),
        init_array(a1),
        store_array(a1, w1, DynamicUInt.from_int(5)),
        add(u1, 5),
    )

    indexes, tape = run_with_tape(program)

    assert tape[indexes[w1[0]]] == 100
    assert tape[indexes[w1[1]]] == 70

    assert tape[indexes[a1] + 13] == 100
    assert tape[indexes[a1] + 15] == 70

    assert tape[indexes[u1]] == 5

    assert sum(tape) == 345

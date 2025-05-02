from quix.bootstrap.dtypes import Array, DynamicUInt, Unit, Wide
from quix.bootstrap.macrocodes import init_array, load_array, store_array
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run_with_tape


def test_load_array_wide_by_int() -> None:
    a1, u1 = Array("a1", length=10), Unit("u1")
    w1 = Wide.from_length("w1", 2)
    program = to_program(
        init_array(a1),
        store_array(a1, DynamicUInt.from_int(258, 2), DynamicUInt.from_int(5)),
        load_array(a1, w1, DynamicUInt.from_int(5)),
        add(u1, 5),
    )

    indexes, tape = run_with_tape(program)

    assert tape[indexes[a1] + 13] == 1
    assert tape[indexes[a1] + 15] == 2

    assert tape[indexes[w1[0]]] == 1
    assert tape[indexes[w1[1]]] == 2

    assert tape[indexes[u1]] == 5

    assert sum(tape) == 11

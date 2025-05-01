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


def test_store_array_int_by_wide() -> None:
    w1 = Wide.from_length("w1", 2)
    a1 = Array("a1", length=1600)
    program = to_program(
        add(w1[0], 1),
        add(w1[1], 70),
        init_array(a1),
        store_array(a1, DynamicUInt.from_int(258), w1),
    )

    indexes, tape = run_with_tape(program)

    assert tape[indexes[w1[0]]] == 1
    assert tape[indexes[w1[1]]] == 70

    index = indexes[a1] + (256 + 70 + 1) * 2

    assert tape[index + 1] == 1
    assert tape[index + 3] == 2

    assert sum(tape) == 74


def test_store_array_int_by_wide_zero_index() -> None:
    w1 = Wide.from_length("w1", 1)
    a1 = Array("a1", length=1600)
    program = to_program(
        add(w1[0], 0),
        init_array(a1),
        store_array(a1, DynamicUInt.from_int(100), w1),
    )

    indexes, tape = run_with_tape(program)

    assert tape[indexes[w1[0]]] == 0

    index = indexes[a1] + 2
    assert tape[index + 1] == 100

    assert sum(tape) == 100


def test_store_array_wide_by_wide_cell_sized() -> None:
    index = Wide.from_length("index", 1)
    store = Wide.from_length("store", 1)
    a1 = Array("a1", length=256)
    program = to_program(
        add(index[0], 50),
        add(store[0], 25),
        init_array(a1),
        store_array(a1, store, index),
    )

    indexes, tape = run_with_tape(program)

    assert tape[indexes[index[0]]] == 50
    assert tape[indexes[store[0]]] == 25

    val_idx = indexes[a1] + (50 + 1) * 2
    assert tape[val_idx + 1] == 25

    assert sum(tape) == 100


def test_store_array_wide_by_wide_cell_sized_granularity_2() -> None:
    index = Wide.from_length("index", 1)
    store = Wide.from_length("store", 1)
    a1 = Array("a1", length=256, granularity=2)
    program = to_program(
        add(index[0], 50),
        add(store[0], 25),
        init_array(a1),
        store_array(a1, store, index),
    )

    indexes, tape = run_with_tape(program)

    assert tape[indexes[index[0]]] == 50
    assert tape[indexes[store[0]]] == 25

    val_idx = indexes[a1] + (50 + 1) * 3
    assert tape[val_idx + 1] == 25

    assert sum(tape) == 100


def test_store_array_wide_by_wide_double() -> None:
    index = Wide.from_length("index", 2)
    store = Wide.from_length("store", 2)
    a1 = Array("a1", length=4092)
    program = to_program(
        add(index[0], 2),
        add(index[1], 75),
        add(store[0], 23),
        add(store[1], 124),
        init_array(a1),
        store_array(a1, store, index),
    )

    indexes, tape = run_with_tape(program)

    assert tape[indexes[index[0]]] == 2
    assert tape[indexes[index[1]]] == 75
    assert tape[indexes[store[0]]] == 23
    assert tape[indexes[store[1]]] == 124

    val_idx = indexes[a1] + (2 * 256 + 75 * 1 + 1) * 2
    assert tape[val_idx + 1] == 23
    assert tape[val_idx + 3] == 124

    assert sum(tape) == 371

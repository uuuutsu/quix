from quix.core.opcodes.opcodes import add, inject, input, loop, output
from quix.core.var import Var


def test_var_add() -> None:
    assert (Var(1) + 1 - 3).build() == [add(1, 1), add(1, -3)]


def test_var_output() -> None:
    assert Var(0).output().build() == [output(0)]


def test_var_input() -> None:
    assert Var(0).input().build() == [input(0)]


def test_var_loop() -> None:
    assert Var(0)[Var(1) + 2].build() == [loop(0, program=[add(1, 2)])]


def test_var_inject() -> None:
    assert Var(0)("#").build() == [inject(0, "#", 0)]

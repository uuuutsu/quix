from io import StringIO

from quix.core.compiler import BFVisitor
from quix.core.compiler.layout import BFMemoryLayout
from quix.core.compiler.pointer import BFPointer
from quix.core.opcodes.dtypes import CoreProgram
from quix.core.opcodes.opcodes import add, inject, input, loop, output

L = BFMemoryLayout


def test_add_pos() -> None:
    assert compile([add(0, 5)], L({0: 1})) == ">+++++"


def test_add_neg() -> None:
    assert compile([add(1, -3)], L({0: 4, 1: 2})) == ">>---"


def test_output() -> None:
    assert compile([output(1)], L({0: 4, 1: 2})) == ">>."


def test_input() -> None:
    assert compile([input(1)], L({0: 4, 1: 2})) == ">>,"


def test_loop() -> None:
    assert compile([loop(3, [add(1, 1)])], L({3: 4, 1: 2})) == ">>>>[<<+>>]"


def test_inject() -> None:
    assert compile([inject(3, "(-_-)", 0), inject(3, "#", 0)], L({3: 4, 0: 2})) == ">>>>(-_-)>>#"


def compile(program: CoreProgram, layout: BFMemoryLayout) -> str:
    buff = StringIO()
    BFVisitor(buff, BFPointer(layout)).visit(program)
    return buff.getvalue()

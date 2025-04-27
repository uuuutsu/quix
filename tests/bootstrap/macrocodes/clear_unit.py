from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocodes import clear_unit
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_clear_unit_simple() -> None:
    u1 = Unit("u1")
    program = to_program(add(u1, 10), clear_unit(u1))

    assert run(program)[u1] == 0

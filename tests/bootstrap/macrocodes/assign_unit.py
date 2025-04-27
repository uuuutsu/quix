from quix.bootstrap.dtypes import Unit
from quix.bootstrap.dtypes.const import UInt8
from quix.bootstrap.macrocodes import assign_unit
from quix.bootstrap.program import to_program

from .utils import run


def test_assignment_short() -> None:
    u1 = Unit("u1")
    for value in range(256):
        program = to_program(assign_unit(u1, UInt8.from_value(value)))
        mem = run(program)

        assert mem[u1] == value
        assert sum(mem.values()) == value

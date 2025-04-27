from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocodes import clear_unit

from .utils import compile_to_bf


def test_clear_unit_simple() -> None:
    u1 = Unit("u1")
    program = clear_unit(u1).builder()

    code = compile_to_bf(program, {u1: 0})
    assert code == "[-]"

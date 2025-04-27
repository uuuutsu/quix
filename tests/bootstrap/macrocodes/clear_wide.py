from quix.bootstrap.dtypes import Wide
from quix.bootstrap.macrocodes import clear_wide

from .utils import compile_to_bf


def test_clear_wide_simple() -> None:
    w1 = Wide.from_length("w1", 2)
    program = clear_wide(w1).builder()

    code = compile_to_bf(program, {w1.units[0]: 0, w1.units[1]: 1})

    assert code == "[-]>[-]"

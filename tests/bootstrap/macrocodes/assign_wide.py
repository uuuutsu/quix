from quix.bootstrap.dtypes import Wide
from quix.bootstrap.dtypes.const import UCell, UDynamic
from quix.bootstrap.macrocodes import assign_wide
from quix.bootstrap.program import to_program

from .utils import run


def test_assign_wide_short() -> None:
    w1 = Wide.from_length("w1", 2)

    program = to_program(
        assign_wide(
            w1,
            UDynamic.from_value(
                (
                    UCell.from_value(50),
                    UCell.from_value(150),
                )
            ),
        )
    )
    mem = run(program)

    assert mem[w1[0]] == 50
    assert mem[w1[1]] == 150
    assert sum(mem.values()) == 200

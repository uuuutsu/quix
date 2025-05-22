from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocodes import switch_wide
from quix.bootstrap.macrocodes.nop import NOP
from quix.bootstrap.program import to_program
from quix.core.opcodes.opcodes import add

from .utils import run


def test_switch_wide() -> None:
    w1 = Wide.from_length("w1", 2)
    program = to_program(
        add(w1[0], 1),
        add(w1[1], 1),
        switch_wide(
            w1,
            {
                UDynamic.from_int(256, 2): add(w1[0], 5),
                UDynamic.from_int(257, 2): add(w1[0], 13),
                UDynamic.from_int(512, 2): add(w1[0], 27),
            },
            NOP,
        ),
    )

    mem = run(program)
    assert mem[w1[0]] == 14
    assert mem[w1[1]] == 1
    assert sum(mem.values()) == 15

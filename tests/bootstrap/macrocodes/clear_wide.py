from quix.bootstrap.dtypes import Wide
from quix.bootstrap.macrocodes import clear_wide
from quix.core.opcodes.opcodes import inject


def test_macrocodes() -> None:
    w1 = Wide.from_length("w1", 1)
    program = clear_wide(w1).builder()

    u1 = w1.units[0]
    assert program == [inject(u1, "[-]", u1, sortable=True)]

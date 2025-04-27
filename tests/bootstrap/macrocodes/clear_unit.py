from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocodes import clear_unit
from quix.core.opcodes.opcodes import inject


def test_macrocodes() -> None:
    u1 = Unit("u1")
    program = clear_unit(u1).builder()

    assert program == [inject(u1, "[-]", u1, sortable=True)]

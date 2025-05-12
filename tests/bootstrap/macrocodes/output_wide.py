from quix.bootstrap.dtypes import Wide
from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.macrocodes import assign_wide, output_wide

from .utils import run_with_output


def test_output_wide_16bit() -> None:
    w1 = Wide.from_length("w1", length=2)
    program = assign_wide(w1, UDynamic.from_int(15689, 2)) | output_wide(w1)

    out = run_with_output(program)

    assert out == "15689"

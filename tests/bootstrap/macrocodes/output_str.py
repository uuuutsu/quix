from quix.bootstrap.dtypes.const import Str
from quix.bootstrap.macrocodes import output_str

from .utils import run_with_output


def test_output_str() -> None:
    program = output_str(Str.from_value("Hello, World!\n"))

    out = run_with_output(program)

    assert out == "Hello, World!\n"

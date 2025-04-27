from quix.bootstrap.dtypes import Wide
from quix.bootstrap.program import ToConvert, macrocode

from .clear_unit import clear_unit


@macrocode
def clear_wide(value: Wide) -> ToConvert:
    return [clear_unit(unit) for unit in value]

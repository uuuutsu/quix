from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes.clear_unit import clear_unit
from quix.bootstrap.program import ToConvert


@macrocode
def clear_wide(value: Wide) -> ToConvert:
    for unit in value:
        yield clear_unit(unit)
    return None

from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import add, inject
from quix.memoptix.opcodes import soft_link

_FLAGS_TABLE: dict[Unit, tuple[Unit, Unit]] = {}


@convert
def opt_call_z_unit(value: Unit, if_: ToConvert, else_: ToConvert, external: bool = True) -> ToConvert:
    if external:
        else_flag, zero = Unit(f"{value.name}_else_z_flag"), Unit(f"{value.name}_zero")
        _FLAGS_TABLE[value] = (else_flag, zero)

        yield soft_link(value, {else_flag: 1, zero: 2})
        yield add(else_flag, 1)
        yield inject(value, "[", value)
        yield else_
        yield inject(else_flag, "[-]]", value)
        yield if_
        yield inject(else_flag, "[[-]", else_flag)
        return inject(zero, "]", zero)

    else_flag, zero = _FLAGS_TABLE[value]
    yield inject(value, "[", value)
    yield else_
    yield inject(value, "[", value)
    yield else_
    yield inject(else_flag, "[-]]", value)
    yield if_
    yield inject(else_flag, "[[-]", else_flag)
    yield inject(zero, "]", zero)

    return None

from quix.unit.opcodes import Unit, Value

from .utils import ToConvert, handler


@handler
def move(from_: Unit, to: dict[Unit, Value]) -> ToConvert:
    if from_ in to:
        raise ValueError("Target unit sequence cannot contain the start unit instance.")

    return from_.to_var()[
        *[unit.to_var() + scale for unit, scale in to.items()],
        from_.to_var() - 1,
    ]

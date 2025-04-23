from typing import overload

from quix.core.opcodes.dtypes import Ref
from quix.core.var import Var
from quix.tools import generate_unique_id


class Unit:
    __slots__ = (
        "_ref",
        "_name",
    )

    def __init__(self, ref: Ref, name: str | None) -> None:
        self._ref = ref
        self._name = name

    def to_var(self) -> Var:
        return Var(self._ref, self._name)

    def __str__(self) -> str:
        return f"Unit( {self._name or self._ref} )"


@overload
def unit(name: str | None) -> Unit: ...
@overload
def unit(name: str | None, ref: Ref) -> Unit: ...
def unit(name: str | None = None, ref: Ref | None = None) -> Unit:
    if ref is None:
        ref = generate_unique_id()
    return Unit(ref=ref, name=name)

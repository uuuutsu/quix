from typing import overload

from quix.core.opcodes.dtypes import Ref
from quix.core.var import Var
from quix.scheduler import Owner
from quix.tools import generate_unique_id


class Unit:
    __slots__ = (
        "ref",
        "name",
    )

    def __init__(self, ref: Ref, name: str | None) -> None:
        self.ref = ref
        self.name = name

    def to_var(self) -> Var:
        return Var(self.ref, self.name)

    def to_owner(self) -> Owner:
        return Owner(ref=self.ref, name=self.name)

    def __str__(self) -> str:
        return f"Unit( {self.name or self.ref} )"


@overload
def unit(name: str | None) -> Unit: ...
@overload
def unit(name: str | None, ref: Ref) -> Unit: ...
def unit(name: str | None = None, ref: Ref | None = None) -> Unit:
    if ref is None:
        ref = generate_unique_id()
    return Unit(ref=ref, name=name)

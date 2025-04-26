from __future__ import annotations

from typing import overload

from quix.core.opcodes.dtypes import Ref
from quix.tools.unique import generate_unique_id


class Owner:
    __slots__ = ("name", "ref")

    def __init__(self, name: str | None = None, *, ref: Ref | None = None) -> None:
        self.name = name
        self.ref = ref or generate_unique_id()

    def __hash__(self) -> int:
        return hash(self.ref)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Owner):
            return False
        return self.ref == value.ref

    def __repr__(self) -> str:
        return f"Owner( {self.name or self.ref} )"


@overload
def owner(name: str | None) -> Owner: ...
@overload
def owner(name: str | None, ref: Ref) -> Owner: ...
def owner(name: str | None = None, ref: Ref | None = None) -> Owner:
    if ref is None:
        ref = generate_unique_id()
    return Owner(ref=ref, name=name)

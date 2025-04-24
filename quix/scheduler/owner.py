from __future__ import annotations

from quix.tools.unique import generate_unique_id


class Owner:
    __slots__ = ("_name", "_ref")

    def __init__(self, name: str | None = None, *, ref: int | None = None) -> None:
        self._name = name
        self._ref = ref or generate_unique_id()

    def __hash__(self) -> int:
        return self._ref

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Owner):
            return False
        return self._ref == value._ref

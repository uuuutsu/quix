from rich.pretty import pretty_repr

from .owner import Owner


class Layout:
    __slots__ = (
        "_mapping",
        "absolute",
        "_reverse_mapping",
    )

    def __init__(self, absolute: bool = False) -> None:
        self._mapping: dict[Owner, int] = {}
        self._reverse_mapping: dict[int, list[Owner]] = {}
        self.absolute = absolute

    def set(self, key: Owner, value: int) -> None:
        self._mapping[key] = value
        self._reverse_mapping.setdefault(value, []).append(key)

    def get_by_owner(self, key: Owner) -> int:
        return self._mapping[key]

    def get_by_idx(self, value: int) -> list[Owner]:
        return self._reverse_mapping[value]

    def __repr__(self) -> str:
        return pretty_repr(self._mapping)

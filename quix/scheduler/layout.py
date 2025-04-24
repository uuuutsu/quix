from collections.abc import Iterable

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

    def __setitem__(self, key: Owner, value: int) -> None:
        self._mapping[key] = value
        self._reverse_mapping.setdefault(value, []).append(key)

    def __getitem__(self, key: Owner) -> int:
        return self._mapping[key]

    def get_by_idx(self, value: int) -> list[Owner]:
        return self._reverse_mapping[value]

    def __contains__(self, item: Owner) -> bool:
        return item in self._mapping

    def items(self) -> Iterable[tuple[Owner, int]]:
        return self._mapping.items()

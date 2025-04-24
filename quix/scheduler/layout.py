from .owner import Owner


class Layout:
    __slots__ = ("_mapping",)

    def __init__(self) -> None:
        self._mapping: dict[Owner, int] = {}

    def __setitem__(self, key: Owner, value: int) -> None:
        self._mapping[key] = value

    def __getitem__(self, key: Owner) -> int:
        return self._mapping[key]

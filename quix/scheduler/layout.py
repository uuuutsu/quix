from .owner import Owner


class Layout:
    __slots__ = ("_mapping", "absolute")

    def __init__(self, absolute: bool = False) -> None:
        self._mapping: dict[Owner, int] = {}
        self.absolute = absolute

    def __setitem__(self, key: Owner, value: int) -> None:
        self._mapping[key] = value

    def __getitem__(self, key: Owner) -> int:
        return self._mapping[key]

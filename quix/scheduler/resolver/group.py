from collections.abc import Iterable

from quix.scheduler.owner import Owner


class Group:
    __slots__ = (
        "_layout",
        "root",
    )

    def __init__(self, root: bool = False) -> None:
        self._layout: dict[Owner, int] = {}
        self.root = root

    def __getitem__(self, key: Owner) -> int:
        return self._layout[key]

    def __setitem__(self, key: Owner, value: int) -> None:
        self._layout[key] = value

    def items(self) -> Iterable[tuple[Owner, int]]:
        return self._layout.items()

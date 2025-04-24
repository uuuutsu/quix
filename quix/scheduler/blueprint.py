from quix.scheduler.owner import Owner

from .constraints import BaseConstraint


class Blueprint:
    __slots__ = (
        "_root",
        "_constraints",
    )

    def __init__(self, root: Owner) -> None:
        self._root = root
        self._constraints: list[BaseConstraint] = []

    def add_constraint(self, constr: BaseConstraint) -> None:
        self._constraints.append(constr)

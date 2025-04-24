from typing import Self

from quix.scheduler.owner import Owner

from .constraints import BaseConstraint


class Blueprint:
    __slots__ = (
        "root",
        "constraints",
    )

    def __init__(self, root: Owner) -> None:
        self.root = root
        self.constraints: list[BaseConstraint] = []

    def add_constraint(self, constr: BaseConstraint) -> Self:
        self.constraints.append(constr)
        return self

    def get_owners(self) -> set[Owner]:
        owners = {
            self.root,
        }
        for constr in self.constraints:
            owners.update(constr.get_owners())
        return owners

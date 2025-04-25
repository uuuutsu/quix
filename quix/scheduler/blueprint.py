from collections.abc import Iterable
from typing import Self

from quix.scheduler.owner import Owner

from .constraints import BaseConstraint


class Blueprint:
    __slots__ = (
        "root",
        "_constraints",
        "hierarchy",
        "domain",
    )

    def __init__(self, root: Owner) -> None:
        self.root = root
        self.hierarchy: dict[Owner, set[Owner]] = {root: set()}
        self._constraints: dict[Owner, set[BaseConstraint]] = {root: set()}
        self.domain: set[type[BaseConstraint]] = set()

    def add_constraint(self, owner: Owner, constr: BaseConstraint) -> Self:
        if owner not in self.hierarchy:
            raise RuntimeError(
                f"Owner {owner} has not been seen in the blueprint yet.Build the blueprint from the root."
            )

        self._constraints.setdefault(owner, set()).add(constr)
        self.domain.add(type(constr))

        owners = constr.get_owners()
        self.hierarchy[owner].update(owners)
        for new_owner in owners:
            self.hierarchy[new_owner] = set()

        return self

    def get_owners(self) -> set[Owner]:
        return set(self.hierarchy.keys())

    def get_constraints(self, owner: Owner) -> set[BaseConstraint]:
        return self._constraints[owner]

    def iter_constr(self) -> Iterable[tuple[Owner, BaseConstraint]]:
        for owner, constrs in self._constraints.items():
            yield from [(owner, constr) for constr in constrs]

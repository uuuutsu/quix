from __future__ import annotations

from collections.abc import Iterable
from typing import Self

from quix.scheduler.owner import Owner

from .constraints import BaseConstraint


class Blueprint:
    __slots__ = (
        "constraints",
        "domain",
    )

    def __init__(self) -> None:
        self.constraints: dict[Owner, list[BaseConstraint]] = {}
        self.domain: set[type[BaseConstraint]] = set()

    def add_constraints(self, owner: Owner, *constrs: BaseConstraint) -> Self:
        for constr in constrs:
            if constr in self.constraints.setdefault(owner, []):
                raise ValueError(f"Constraint {constr} already exist for owner {owner}")

            self.constraints[owner].append(constr)
            self.domain.add(type(constr))

        return self

    def get_owners(self) -> set[Owner]:
        owners = set()
        for owner, constrs in self.constraints.items():
            owners.add(owner)
            for constr in constrs:
                owners.update(constr.get_owners())
        return owners

    def combine(self, other: Blueprint) -> Blueprint:
        new_bp = Blueprint()
        new_bp.constraints = self.constraints | other.constraints
        new_bp.domain = self.domain | other.domain
        return new_bp

    def get_constraints(self, owner: Owner) -> list[BaseConstraint]:
        return self.constraints[owner]

    def iter_constr(self) -> Iterable[tuple[Owner, BaseConstraint]]:
        for owner, constrs in self.constraints.items():
            yield from [(owner, constr) for constr in constrs]

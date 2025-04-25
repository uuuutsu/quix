from __future__ import annotations

import mip  # type: ignore

from quix.exceptions.scheduler import IndexIsNotYetResolvedError
from quix.scheduler.owner import Owner


def owner_to_str_key(owner: Owner) -> str:
    return str(hash(owner))


class Model:
    __slots__ = ("model", "_owners")

    def __init__(self) -> None:
        self.model = mip.Model()
        self._owners: list[Owner] = []

    def add_var(
        self,
        owner: Owner | None,
        lb: mip.numbers.Real = 0.0,
        ub: mip.numbers.Real = mip.INF,
        obj: mip.numbers.Real = 0.0,
        var_type: str = mip.CONTINUOUS,
        column: mip.Column | None = None,
    ) -> mip.Var:
        if owner:
            self._owners.append(owner)
        return self.model.add_var(
            "" if owner is None else owner_to_str_key(owner),
            lb=lb,
            ub=ub,
            obj=obj,
            var_type=var_type,
            column=column,
        )

    def add_constr(
        self,
        lin_expr: mip.LinExpr,
        name: str = "",
        priority: mip.ConstraintPriority | None = None,
    ) -> mip.Constr:
        return self.model.add_constr(
            lin_expr=lin_expr,
            name=name,
            priority=priority,
        )

    def add_sos(self, sos: list[tuple[mip.Var, mip.numbers.Real]], sos_type: int) -> None:
        self.model.add_sos(sos=sos, sos_type=sos_type)

    def get_var(self, owner: Owner) -> mip.Var | None:
        return self.model.var_by_name(owner_to_str_key(owner))

    def optimize(
        self,
        max_seconds: mip.numbers.Real = mip.INF,
        max_nodes: int = mip.INT_MAX,
        max_solutions: int = mip.INT_MAX,
        max_seconds_same_incumbent: mip.numbers.Real = mip.INF,
        max_nodes_same_incumbent: int = mip.INT_MAX,
        relax: bool = False,
        verbose: int = 0,
    ) -> mip.OptimizationStatus:
        self.model.verbose = verbose
        return self.model.optimize(
            max_seconds=max_seconds,
            max_nodes=max_nodes,
            max_solutions=max_solutions,
            max_seconds_same_incumbent=max_seconds_same_incumbent,
            max_nodes_same_incumbent=max_nodes_same_incumbent,
            relax=relax,
        )

    def get_mapping(self) -> dict[Owner, int]:
        indexes = {}
        for owner in self._owners:
            index = self.get_var(owner)
            if index is None:
                raise IndexIsNotYetResolvedError(owner)
            indexes[owner] = int(index.x)

        return indexes

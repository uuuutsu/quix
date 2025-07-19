from __future__ import annotations

import mip  # type: ignore

from quix.exceptions.scheduler import NodeIndexIsNotYetResolvedError, UnknownNodeException
from quix.memoptixv2.scheduler.tree import Node
from quix.tools import silence


def node_to_str_key(node: Node) -> str:
    return str(hash(node))


class Model:
    __slots__ = ("_mip_model", "_nodes")

    def __init__(self) -> None:
        self._mip_model = mip.Model()
        self._nodes: list[Node] = []

    def add_var(
        self,
        node: Node | None,
        lb: float = 0.0,
        ub: float = float("inf"),
        obj: float = 0.0,
        var_type: str = mip.INTEGER,
        column: mip.Column | None = None,
    ) -> mip.Var:
        if node:
            self._nodes.append(node)
        return self._mip_model.add_var(
            "" if node is None else node_to_str_key(node),
            lb=lb,  # type: ignore
            ub=ub,  # type: ignore
            obj=obj,  # type: ignore
            var_type=var_type,
            column=column,  # type: ignore
        )

    def add_constr(
        self,
        lin_expr: mip.LinExpr,
        name: str = "",
        priority: mip.ConstraintPriority | None = None,
    ) -> mip.Constr:
        return self._mip_model.add_constr(
            lin_expr=lin_expr,
            name=name,
            priority=priority,
        )

    def add_sos(self, sos: list[tuple[mip.Var, mip.numbers.Real]], sos_type: int) -> None:
        self._mip_model.add_sos(sos=sos, sos_type=sos_type)

    def optimize(
        self,
        max_seconds: mip.numbers.Real = mip.INF,  # type: ignore
        max_nodes: int = mip.INT_MAX,
        max_solutions: int = mip.INT_MAX,
        max_seconds_same_incumbent: mip.numbers.Real = mip.INF,  # type: ignore
        max_nodes_same_incumbent: int = mip.INT_MAX,
        relax: bool = False,
        verbose: int = 0,
    ) -> mip.OptimizationStatus:
        self._mip_model.verbose = verbose
        if verbose == 0:
            with silence():
                return self._mip_model.optimize(
                    max_seconds=max_seconds,
                    max_nodes=max_nodes,
                    max_solutions=max_solutions,
                    max_seconds_same_incumbent=max_seconds_same_incumbent,
                    max_nodes_same_incumbent=max_nodes_same_incumbent,
                    relax=relax,
                )
        return self._mip_model.optimize(
            max_seconds=max_seconds,
            max_nodes=max_nodes,
            max_solutions=max_solutions,
            max_seconds_same_incumbent=max_seconds_same_incumbent,
            max_nodes_same_incumbent=max_nodes_same_incumbent,
            relax=relax,
        )

    def get_var_by_node(self, node: Node) -> mip.Var:
        var = self._mip_model.var_by_name(node_to_str_key(node))
        if var is None:
            raise UnknownNodeException(node)
        return var

    def get_mapping(self) -> dict[Node, int]:
        indexes = {}
        for node in self._nodes:
            index = self.get_var_by_node(node)
            if index.x is None:
                raise NodeIndexIsNotYetResolvedError(node)
            indexes[node] = int(index.x)  # type: ignore

        return indexes

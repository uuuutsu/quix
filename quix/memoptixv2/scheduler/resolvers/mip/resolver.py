from typing import override

from mip import OptimizationStatus  # type: ignore

from quix.memoptixv2.scheduler.layout import Layout
from quix.memoptixv2.scheduler.resolvers.base import Resolver
from quix.memoptixv2.scheduler.tree import Array, HardLink, Index, Node, SoftLink, flatten_node, get_constraint_groups

from .exprs import expr_index, expr_lifecycle, expr_links
from .model import Model


class MIPResolver(Resolver):
    __slots__ = ()

    __domain__ = {Array, Index, HardLink, SoftLink}

    @override
    def __call__(self, root: Node) -> Layout:
        model = Model()

        for node in flatten_node(root):
            model.add_var(node)
        mappers = get_constraint_groups(root)

        expr_index(mappers.get(Index, {}), model)  # type: ignore
        expr_lifecycle(mappers.get(Array, {}), model)  # type: ignore
        expr_links(mappers.get(HardLink, {}), mappers.get(SoftLink, {}), model)  # type: ignore

        status = model.optimize()
        match status:
            case OptimizationStatus.INFEASIBLE:
                raise RuntimeError(f"{model!r} cannot be optimized.")
        return Layout(model.get_mapping(), node=root)

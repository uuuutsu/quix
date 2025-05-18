from typing import override

from mip import OptimizationStatus  # type: ignore

from quix.memoptix.scheduler.blueprint import Blueprint
from quix.memoptix.scheduler.constraints import Array, HardLink, Index, LifeCycle, SoftLink
from quix.memoptix.scheduler.layout import Layout
from quix.memoptix.scheduler.resolvers.base import Resolver
from quix.memoptix.scheduler.utils import get_constraint_mappers

from .exprs import expr_index, expr_lifecycle, expr_links
from .model import Model


class MIPResolver(Resolver):
    __slots__ = ()

    __domain__ = {Array, Index, LifeCycle, HardLink, SoftLink}

    @override
    def __call__(self, blueprint: Blueprint) -> Layout:
        model = Model()

        for owner in blueprint.get_owners():
            model.add_var(owner)
        mappers = get_constraint_mappers(blueprint)

        expr_index(mappers.get(Index, {}), model)  # type: ignore
        expr_lifecycle(mappers.get(LifeCycle, {}), mappers.get(Array, {}), model)  # type: ignore
        expr_links(mappers.get(HardLink, {}), mappers.get(SoftLink, {}), model)  # type: ignore

        status = model.optimize()
        match status:
            case OptimizationStatus.INFEASIBLE:
                raise RuntimeError(f"{model!r} cannot be optimized.")
        return Layout(blueprint, model.get_mapping())

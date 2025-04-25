from typing import override

from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import Array, HardLink, Index, LifeCycle, SoftLink
from quix.scheduler.layout import Layout
from quix.scheduler.resolvers.base import Resolver

from .exprs import expr_index, expr_lifecycle, expr_links
from .model import Model
from .utils import get_constraint_mappers


class MIPResolver(Resolver):
    __slots__ = ()

    __domain__ = {Array, Index, LifeCycle, HardLink, SoftLink}

    @override
    def __call__(self, blueprint: Blueprint) -> Layout:
        model = Model()
        layout = Layout(Index in blueprint.domain)

        for owner in blueprint.get_owners():
            model.add_var(owner)

        mappers = get_constraint_mappers(blueprint)
        expr_index(mappers.get(Index, {}), model)  # type: ignore
        expr_lifecycle(mappers.get(LifeCycle, {}), mappers.get(Array, {}), model)  # type: ignore
        expr_links(mappers.get(HardLink, {}), mappers.get(SoftLink, {}), model)  # type: ignore

        model.optimize()
        for owner, index in model.get_mapping().items():
            layout.set(owner, index)

        return layout

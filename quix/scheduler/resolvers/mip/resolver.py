from typing import override

from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import HardLink, Index, LifeCycle, Reserve, SoftLink
from quix.scheduler.layout import Layout
from quix.scheduler.resolvers.base import Resolver

from .exprs import EXPR_REGISTRY
from .model import Model
from .utils import get_constraint_mappers


class MIPResolver(Resolver):
    __slots__ = ()

    __domain__ = {Reserve, Index, LifeCycle, HardLink, SoftLink}

    @override
    def __call__(self, blueprint: Blueprint) -> Layout:
        model = Model()
        layout = Layout(Index in blueprint.domain)

        for owner in blueprint.get_owners():
            model.add_var(owner)

        mappers = get_constraint_mappers(blueprint)
        for type, mapper in mappers.items():
            EXPR_REGISTRY[type](mapper, model)

        model.optimize()
        for owner, index in model.get_mapping().items():
            layout.set(owner, index)

        return layout

from typing import override

import mip  # type: ignore

from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import HardLink, Index, LifeCycle, Reserve, SoftLink
from quix.scheduler.layout import Layout
from quix.scheduler.owner import Owner
from quix.scheduler.resolvers.base import Resolver

from .handlers import handle_index
from .model import Model


class MIPResolver(Resolver):
    __slots__ = ()

    __domain__ = {Reserve, Index, LifeCycle, HardLink, SoftLink}

    @override
    def __call__(self, blueprint: Blueprint) -> Layout:
        model = Model()

        owner2var: dict[Owner, mip.Var] = {}
        for owner in blueprint.get_owners():
            owner2var[owner] = model.add_var(owner)

        for owner, constr in blueprint.iter_constr():
            match constr:
                case Index():
                    handle_index(owner2var[owner], model, constr)

        layout = Layout(Index in blueprint.domain)
        model.optimize()
        for owner, index in model.get_mapping().items():
            layout.set(owner, index)

        return layout

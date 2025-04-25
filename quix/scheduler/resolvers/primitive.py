from typing import override

from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import Array, Index, LifeCycle
from quix.scheduler.layout import Layout
from quix.scheduler.owner import Owner

from .base import Resolver


class PrimitiveResolver(Resolver):
    __slots__ = ()

    __domain__ = {Index, LifeCycle, Array}

    @override
    def __call__(self, blueprint: Blueprint) -> Layout:
        layout: dict[Owner, int] = {blueprint.root: 0}
        absolute: bool = False

        for owner, constr in blueprint.iter_constr():
            match constr:
                case Index():
                    absolute = True
                    layout[owner] = constr.index
                    break

        return Layout(blueprint, layout, absolute)

from typing import override

from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import Array, Index, LifeCycle
from quix.scheduler.layout import Layout

from .base import Resolver


class PrimitiveResolver(Resolver):
    __slots__ = ()

    __domain__ = {Index, LifeCycle, Array}

    @override
    def __call__(self, blueprint: Blueprint) -> Layout:
        layout = Layout()
        if Index not in blueprint.domain:
            layout.set(blueprint.root, 0)
            return layout

        for owner, constr in blueprint.iter_constr():
            match constr:
                case Index():
                    layout.absolute = True
                    layout.set(owner, constr.index)
                    return layout

        raise NotImplementedError("No available")

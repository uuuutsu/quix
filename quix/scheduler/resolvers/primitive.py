from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import Index, LifeCycle, Reserve
from quix.scheduler.layout import Layout

from .base import Resolver


class PrimitiveResolver(Resolver):
    __slots__ = ()

    __signature__ = {Index, LifeCycle, Reserve}

    def __call__(self, blueprint: Blueprint) -> Layout:
        layout = Layout()
        if Index not in blueprint.signature:
            layout.set(blueprint.root, 0)
            return layout

        for constr in blueprint.get_constraints(blueprint.root):
            match constr:
                case Index():
                    layout.absolute = True
                    layout.set(blueprint.root, constr.index)
                    return layout

        raise NotImplementedError("No available")

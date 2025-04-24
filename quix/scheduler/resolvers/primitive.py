from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import Index, LifeCycle, Reserve
from quix.scheduler.layout import Layout

from .base import Resolver


class PrimitiveResolver(Resolver):
    __slots__ = ()

    __signature__ = {Index, LifeCycle, Reserve}

    def __call__(self, blueprint: Blueprint) -> Layout:
        raise NotImplementedError

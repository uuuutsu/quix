from typing import override

from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import HardLink, Index, LifeCycle, Reserve, SoftLink
from quix.scheduler.layout import Layout
from quix.scheduler.resolvers.base import Resolver


class MIPResolver(Resolver):
    __slots__ = ()

    __signature__ = {Reserve, Index, LifeCycle, HardLink, SoftLink}

    @override
    def __call__(self, blueprint: Blueprint) -> Layout:
        raise NotImplementedError

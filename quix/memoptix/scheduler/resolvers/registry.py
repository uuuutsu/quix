from quix.memoptix.scheduler.blueprint import Blueprint
from quix.memoptix.scheduler.layout import Layout
from quix.memoptix.scheduler.utils import Matcher, inclusion_matcher

from .base import Resolver
from .mip import MIPResolver
from .primitive import PrimitiveResolver


class ResolverRegistry:
    __slots__ = (
        "_matcher",
        "_resolvers",
    )

    def __init__(self, matcher: Matcher = inclusion_matcher) -> None:
        self._matcher = matcher
        self._resolvers: list[Resolver] = []

    def __call__(self, blueprint: Blueprint) -> Layout:
        domains = [resolver.__domain__ for resolver in self._resolvers]
        match = self._matcher(blueprint.domain, domains)

        if match is None:
            raise RuntimeError(f"No resolver was found to handle: {blueprint.domain}")

        return self._resolvers[match](blueprint)

    def register(self, resolver: Resolver) -> None:
        self._resolvers.append(resolver)


def create_resolver_registry() -> ResolverRegistry:
    registry = ResolverRegistry()
    registry.register(PrimitiveResolver())
    registry.register(MIPResolver())
    return registry

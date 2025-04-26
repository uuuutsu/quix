import math
from collections.abc import Callable

from quix.memoptix.scheduler.blueprint import Blueprint
from quix.memoptix.scheduler.constraints import BaseConstraint
from quix.memoptix.scheduler.layout import Layout

from .base import Resolver
from .mip import MIPResolver
from .primitive import PrimitiveResolver

type Domain = set[type[BaseConstraint]]
type Matcher = Callable[[Domain, list[Domain]], int | None]


def _inclusion_matcher(to_match: Domain, registry: list[Domain]) -> int | None:
    curr_match: int | None = None
    curr_length: float = math.inf

    for idx, domain in enumerate(registry):
        if domain.difference(to_match):
            continue
        if len(domain) < curr_length:
            curr_length = len(domain)
            curr_match = idx

    if curr_match:
        return curr_match

    return None


class ResolverRegistry:
    __slots__ = (
        "_matcher",
        "_resolvers",
    )

    def __init__(self, matcher: Matcher = _inclusion_matcher) -> None:
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

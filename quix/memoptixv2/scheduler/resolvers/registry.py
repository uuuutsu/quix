import math
from collections.abc import Callable

from quix.memoptixv2.scheduler.layout import Layout
from quix.memoptixv2.scheduler.tree import Domain, Node, get_domain

from .base import Resolver
from .mip import MIPResolver
from .primitive import PrimitiveResolver

type Matcher = Callable[[Domain, list[Domain]], int | None]


def inclusion_matcher(to_match: Domain, registry: list[Domain]) -> int | None:
    curr_match: int | None = None
    curr_length: float = math.inf

    for idx, domain in enumerate(registry):
        if to_match - domain:
            continue
        if len(domain) < curr_length:
            curr_length = len(domain)
            curr_match = idx

    if curr_match is not None:
        return curr_match

    return None


class ResolverRegistry:
    __slots__ = (
        "_matcher",
        "_resolvers",
    )

    def __init__(self, matcher: Matcher = inclusion_matcher) -> None:
        self._matcher = matcher
        self._resolvers: list[Resolver] = []

    def __call__(self, root: Node) -> Layout:
        domains = [resolver.__domain__ for resolver in self._resolvers]
        root_domain = get_domain(root)
        match = self._matcher(root_domain, domains)

        if match is None:
            raise RuntimeError(f"No resolver was found to handle: {root_domain}")

        return self._resolvers[match](root)

    def register(self, resolver: Resolver) -> None:
        self._resolvers.append(resolver)


def create_resolver_registry() -> ResolverRegistry:
    registry = ResolverRegistry()
    registry.register(PrimitiveResolver())
    registry.register(MIPResolver())
    return registry

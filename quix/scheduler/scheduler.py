from quix.scheduler.blueprint import Blueprint
from quix.scheduler.layout import Layout
from quix.scheduler.resolvers.registry import ResolverRegistry
from quix.scheduler.sliders.registry import SliderRegistry


class Scheduler:
    __slots__ = (
        "_resolver_registry",
        "_slider_registry",
    )

    def __init__(self, resolver_registry: ResolverRegistry, slider_registry: SliderRegistry) -> None:
        self._resolver_registry = resolver_registry
        self._slider_registry = slider_registry

    def schedule(self, *bps: Blueprint) -> Layout:
        layouts = []
        for bp in bps:
            layouts.append(self._resolver_registry(bp))

        while len(layouts) > 1:
            layouts.append(self._slider_registry(layouts.pop(), layouts.pop()))

        return layouts[0]

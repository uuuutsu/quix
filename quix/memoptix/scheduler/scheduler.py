from quix.memoptix.scheduler.layout import Layout
from quix.memoptix.scheduler.resolvers.registry import ResolverRegistry
from quix.memoptix.scheduler.sliders.registry import SliderRegistry
from quix.memoptix.scheduler.tree import Node


class Scheduler:
    __slots__ = (
        "_resolver_registry",
        "_slider_registry",
    )

    def __init__(self, resolver_registry: ResolverRegistry, slider_registry: SliderRegistry) -> None:
        self._resolver_registry = resolver_registry
        self._slider_registry = slider_registry

    def schedule(self, *nodes: Node) -> Layout:
        layouts = []
        for node in nodes:
            layouts.append(self._resolver_registry(node))

        while len(layouts) > 1:
            layouts.append(self._slider_registry(layouts.pop(), layouts.pop()))

        return layouts[0]

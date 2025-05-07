from typing import Self, override

from quix.bootstrap.program import ToConvert, convert

from .component import Component


class Layout(Component):
    __slots__ = ("_components",)

    def __init__(self) -> None:
        self._components: dict[Component, int] = {}

    def add_component(self, comp: Component, offset: int) -> Self:
        self._components[comp] = offset
        return self

    @convert
    @override
    def create(self, memory_index: int) -> ToConvert:
        curr_idx = memory_index
        for comp, off in self._components.items():
            yield comp.create(curr_idx + off)
            curr_idx += off + comp.size()

        return None

    @override
    def size(self) -> int:
        return max(self._components.values()) - min(self._components.values())

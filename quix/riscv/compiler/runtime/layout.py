from typing import override

from quix.bootstrap.program import ToConvert, convert

from .component import Component


class Layout(Component):
    __slots__ = ("_components",)

    def __init__(self) -> None:
        self._components: dict[int, Component] = {}

    def add_component(self, comp: Component, offset: int) -> None:
        self._components[offset] = comp

    @convert
    @override
    def create(self, memory_index: int) -> ToConvert:
        curr_idx = memory_index
        for off, comp in self._components.items():
            yield comp.create(curr_idx + off)
            curr_idx += off + comp.size()

        return None

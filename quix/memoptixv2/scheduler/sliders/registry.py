from quix.memoptixv2.scheduler.layout import Layout
from quix.memoptixv2.scheduler.tree import Node, get_domain
from quix.memoptixv2.scheduler.utils import Matcher, inclusion_matcher

from .base import Slider
from .simple import SimpleSlider


class SliderRegistry:
    __slots__ = (
        "_matcher",
        "_sliders",
    )

    def __init__(self, matcher: Matcher = inclusion_matcher) -> None:
        self._matcher = matcher
        self._sliders: list[Slider] = []

    def __call__(self, left: Layout, right: Layout) -> dict[Node, int]:
        domains = [slider.__domain__ for slider in self._sliders]
        match = self._matcher(get_domain(left.node) | get_domain(left.node), domains)

        if match is None:
            raise RuntimeError(f"No slider found to handle: {left} + {right}")

        return self._sliders[match](left, right)

    def register(self, slider: Slider) -> None:
        self._sliders.append(slider)


def create_slider_registry() -> SliderRegistry:
    registry = SliderRegistry()
    registry.register(SimpleSlider())
    return registry

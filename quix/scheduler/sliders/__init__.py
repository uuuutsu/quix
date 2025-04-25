__all__ = (
    "Slider",
    "SimpleSlider",
    "SliderRegistry",
    "create_slider_registry",
)

from .base import Slider
from .registry import SliderRegistry, create_slider_registry
from .simple import SimpleSlider

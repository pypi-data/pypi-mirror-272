from rich.abc import RichRenderable

from spellbound.utils.class_value_finder import ClassValueFinder
from spellbound.utils.apply import ApplyMixin
from spellbound.utils.richer.core.renderer import RichRenderer


class Richer(ApplyMixin):
    def __init__(self):
        self._renderers = ClassValueFinder()

    def register(self, renderer_class):
        """
        Register a Renderer class.

        Args:
            renderer_class (type): Renderer class to register.

        Returns:
            Richer: self
        """
        if not issubclass(renderer_class, RichRenderer):
            raise TypeError(
                "Cannot register a Renderer class that is not a subclass of RichRenderer"
            )

        value_class = renderer_class.value_class()
        if value_class is None:
            raise ValueError("Cannot register a Renderer without a value_class")

        self._renderers[value_class] = renderer_class(self)
        return self

    def render(self, value, fallback_renderer=None):
        """
        Render a value to a RichRenderable.

        Args:
            value (object): value to render
            fallback_renderer (Callable, optional): Renderer to use if no Renderer is found. Defaults to None.

        Returns:
            RichRenderable: rich's Renderable or None if no Renderer is found
        """

        if isinstance(value, RichRenderable):
            return value

        renderer = self._renderers.find_by_instance(value)
        if renderer:
            return renderer(value)
        if fallback_renderer:
            return fallback_renderer(value)
        return None

import abc


class RichRenderer(abc.ABC):
    """
    A callable that converts an instance to a RichRenderable.
    """

    @classmethod
    def value_class(cls):
        """
        Get the class that this renderer can render.
        """
        return None

    def __init__(self, richer):
        """
        Args:
            richer (Richer): Richer instance
        """
        super().__init__()
        self.richer = richer

    @abc.abstractmethod
    def __call__(self, value):
        """
        Convert the instance to a RichRenderable.

        Args:
            instance (object): instance to convert

        Returns:
            RichRenderable: rich Renderable
        """

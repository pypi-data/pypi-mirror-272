class ApplyMixin:
    def apply(self, func, *args, **kwargs):
        """
        Apply a function to the object and return self.
        This could be use to fluently apply presets.

        Example:
        >>> class Registry(ApplyMixin):
        >>>    ...
        >>>
        >>> registry = Registry()
        >>> def common_preset(registry):
        >>>    registry.set_value("a", 1)
        >>>    registry.set_value("b", 2)
        >>>    registry.set_value("c", 3)
        >>> registry.apply(common_preset)

        Args:
            func (Callable): function to apply

        Returns:
            typing_extensions.Self: self

        """
        func(self, *args, **kwargs)
        return self

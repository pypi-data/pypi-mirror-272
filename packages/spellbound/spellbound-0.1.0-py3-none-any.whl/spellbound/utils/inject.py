import abc

class Injector(abc.ABC):
    @abc.abstractmethod
    def get(self, key, *args, **kwargs):
        """
        Get a value from the injector.

        Args:
            key (str): key to get

        Returns:
            Any: value
        """

class FakeInjector(Injector):
    def get(self, key, *args, **kwargs):
        return key(*args, **kwargs)

import abc


class Interceptor(abc.ABC):
    def __init__(self):
        self._emitter = None

    @abc.abstractmethod
    def _configure(self, when):
        """
        Configure connection to an emitter.

        Args:
            when (Callable[str, Callable]): function to attach/detach event listeners to/from the emitter
        """

    def _attach(self, emitter):
        self._configure(emitter.on)

    def attach(self, emitter):
        """
        Attach to an emitter.

        Args:
            emitter (EventEmitter): emitter to attach to

        Returns:
            Interceptor: self
        """
        if self._emitter:
            raise RuntimeError("Interceptor is already attached to an Emitter.")
        self._emitter = emitter
        self._attach(emitter)
        return self

    def _detach(self, emitter):
        self._configure(emitter.off)

    def detach(self):
        """
        Detach from an emitter.

        Returns:
            Interceptor: self
        """
        if self._emitter:
            self._detach(self._emitter)
            self._emitter = None
        return self

    def __del__(self):
        self.detach()

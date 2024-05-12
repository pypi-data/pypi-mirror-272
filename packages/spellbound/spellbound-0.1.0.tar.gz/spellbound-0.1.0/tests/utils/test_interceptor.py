import unittest
from unittest.mock import MagicMock

from spellbound.utils.emitter import Emitter
from spellbound.utils.interceptor import Interceptor


class ExampleInterceptor(Interceptor):
    def __init__(self):
        super().__init__()
        self._handler = MagicMock()

    def _configure(self, when):
        when("test-event1", self._handler)


class TestInterceptor(unittest.TestCase):
    def setUp(self):
        self.emitter = Emitter()
        self.interceptor = ExampleInterceptor()

    def test_attach(self):
        self.interceptor.attach(self.emitter)
        self.emitter.trigger("test-event1", "arg1", "arg2")
        self.interceptor._handler.assert_called_once()

    def test_detach(self):
        self.interceptor.attach(self.emitter)
        self.interceptor.detach()
        self.emitter.trigger("test-event1", "arg1", "arg2")
        self.interceptor._handler.assert_not_called()

    def test_attach_twice(self):
        self.interceptor.attach(self.emitter)
        with self.assertRaises(RuntimeError):
            self.interceptor.attach(self.emitter)

    def test_detach_twice(self):
        self.interceptor.attach(self.emitter)
        self.interceptor.detach()
        self.interceptor.detach()

import unittest
from unittest.mock import MagicMock

from spellbound.utils.emitter import Emitter


class TestEmitter(unittest.TestCase):
    def test_on(self):
        emitter = Emitter()
        callback = MagicMock()

        emitter.on("test_event", callback)
        self.assertIn(callback, emitter.listeners["test_event"])

    def test_off(self):
        emitter = Emitter()
        callback = MagicMock()

        emitter.on("test_event", callback)
        emitter.off("test_event", callback)
        self.assertNotIn(callback, emitter.listeners["test_event"])

    def test_trigger(self):
        emitter = Emitter()
        callback1 = MagicMock()
        callback2 = MagicMock()

        emitter.on("test_event", callback1)
        emitter.on("test_event", callback2)
        emitter.trigger("test_event", "arg1", "arg2", kwarg1="value1", kwarg2="value2")

        callback1.assert_called_once_with(
            "arg1", "arg2", kwarg1="value1", kwarg2="value2"
        )
        callback2.assert_called_once_with(
            "arg1", "arg2", kwarg1="value1", kwarg2="value2"
        )

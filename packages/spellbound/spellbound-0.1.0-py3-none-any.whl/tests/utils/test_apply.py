import unittest

from spellbound.utils.apply import ApplyMixin


class TestApplyMixin(unittest.TestCase):
    def test_apply(self):
        class Applicable(ApplyMixin):
            def __init__(self):
                self.x = 0

        a = Applicable()

        def preset(a):
            a.x = 1

        result = a.apply(preset)
        self.assertIs(result, a)
        self.assertEqual(result.x, 1)

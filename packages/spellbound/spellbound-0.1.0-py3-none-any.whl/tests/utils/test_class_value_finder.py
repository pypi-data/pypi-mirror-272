import unittest

from spellbound.utils.class_value_finder import ClassValueFinder


class Fath:
    pass


class Father(Fath):
    pass


class GodFather(Father):
    pass


class Mother:
    pass


class TestClassValueFinder(unittest.TestCase):
    def test_find_by_class(self):
        l = ClassValueFinder()
        l[Fath] = "Fath"
        l[GodFather] = "GodFather"

        self.assertEqual(l.find_by_class(Fath), "Fath")
        self.assertEqual(l.find_by_class(Father), "Fath")
        self.assertEqual(l.find_by_class(GodFather), "GodFather")
        self.assertEqual(l.find_by_class(Mother), None)

    def test_find_by_instance(self):
        l = ClassValueFinder()
        l[Fath] = "Fath"
        l[GodFather] = "GodFather"

        self.assertEqual(l.find_by_instance(Fath()), "Fath")
        self.assertEqual(l.find_by_instance(Father()), "Fath")
        self.assertEqual(l.find_by_instance(GodFather()), "GodFather")
        self.assertEqual(l.find_by_instance(Mother()), None)

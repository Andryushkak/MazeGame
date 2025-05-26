import unittest
from app.coffee.factory import CoffeeFactory


class TestFactoryErrors(unittest.TestCase):
    def test_invalid_coffee_type(self):
        factory = CoffeeFactory()
        with self.assertRaises(ValueError):
            factory.create_coffee("Mocha")  # не існує такого типу

    def test_factory_creates_all_types(self):
        factory = CoffeeFactory()
        for name in ["Espresso", "Latte", "Cappuccino"]:
            coffee = factory.create_coffee(name)
            self.assertIsNotNone(coffee)

    def test_factory_case_insensitive_fail(self):
        factory = CoffeeFactory()
        with self.assertRaises(ValueError):
            factory.create_coffee("espresso")  # lowercase — помилка

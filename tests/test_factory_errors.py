
import unittest
from app.coffee.factory import CoffeeFactory

class TestFactoryErrors(unittest.TestCase):
    def test_invalid_coffee_type(self):
        factory = CoffeeFactory()
        with self.assertRaises(ValueError):
            factory.create_coffee("Mocha")

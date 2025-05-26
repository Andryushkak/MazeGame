
import unittest
from app.coffee.factory import CoffeeFactory
from app.coffee.decorators import Milk, Chocolate, Syrup

class TestDecorators(unittest.TestCase):
    def setUp(self):
        self.factory = CoffeeFactory()

    def test_espresso_with_milk_and_syrup(self):
        coffee = self.factory.create_coffee("Espresso")
        coffee = Milk(Syrup(coffee))
        self.assertIn("Milk", coffee.get_description())
        self.assertIn("Syrup", coffee.get_description())
        self.assertAlmostEqual(coffee.cost(), 1.5 + 0.3 + 0.5)

    def test_cappuccino_with_all(self):
        coffee = self.factory.create_coffee("Cappuccino")
        coffee = Milk(Chocolate(Syrup(coffee)))
        self.assertIn("Milk", coffee.get_description())
        self.assertIn("Chocolate", coffee.get_description())
        self.assertIn("Syrup", coffee.get_description())
        self.assertAlmostEqual(coffee.cost(), 2.5 + 0.3 + 0.4 + 0.5)

    def test_double_milk(self):
        coffee = self.factory.create_coffee("Latte")
        coffee = Milk(Milk(coffee))
        self.assertEqual(coffee.get_description().count("Milk"), 2)
        self.assertAlmostEqual(coffee.cost(), 2.0 + 0.3 + 0.3)

def test_chocolate_cost(self):
    coffee = Chocolate(self.factory.create_coffee("Espresso"))
    self.assertAlmostEqual(coffee.cost(), 1.5 + 0.4)

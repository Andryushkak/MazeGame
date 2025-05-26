
import unittest
from app.coffee.factory import CoffeeFactory
from app.coffee.decorators import Milk, Chocolate, Syrup
from app.order.order import Order
from app.order.observer import Customer

class TestCoffeeFactory(unittest.TestCase):
    def setUp(self):
        self.factory = CoffeeFactory()

    def test_create_espresso(self):
        coffee = self.factory.create_coffee("Espresso")
        self.assertEqual(coffee.get_description(), "Espresso")
        self.assertEqual(coffee.cost(), 1.5)

    def test_create_latte(self):
        coffee = self.factory.create_coffee("Latte")
        self.assertEqual(coffee.get_description(), "Latte")
        self.assertEqual(coffee.cost(), 2.0)

    def test_create_cappuccino(self):
        coffee = self.factory.create_coffee("Cappuccino")
        self.assertEqual(coffee.get_description(), "Cappuccino")
        self.assertEqual(coffee.cost(), 2.5)

    def test_add_milk(self):
        coffee = self.factory.create_coffee("Espresso")
        coffee = Milk(coffee)
        self.assertIn("Milk", coffee.get_description())
        self.assertAlmostEqual(coffee.cost(), 1.8)

    def test_add_chocolate_and_syrup(self):
        coffee = self.factory.create_coffee("Latte")
        coffee = Chocolate(Syrup(coffee))
        self.assertIn("Chocolate", coffee.get_description())
        self.assertIn("Syrup", coffee.get_description())
        self.assertAlmostEqual(coffee.cost(), 2.0 + 0.4 + 0.5)

class TestOrderObserver(unittest.TestCase):
    def test_order_observer_notification(self):
        order = Order()
        customer = Customer("TestUser")
        order.add_observer(customer)
        order.set_status("Preparing")
        order.set_status("Ready")
        self.assertEqual(order.status, "Ready")

if __name__ == "__main__":
    unittest.main()

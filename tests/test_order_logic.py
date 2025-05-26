
import unittest
from app.order.order import Order
from app.order.observer import Customer

class TestOrderLogic(unittest.TestCase):
    def test_observer_added(self):
        order = Order()
        customer = Customer("Ivan")
        order.add_observer(customer)
        self.assertIn(customer, order.observers)

    def test_observer_removed(self):
        order = Order()
        customer = Customer("Ivan")
        order.add_observer(customer)
        order.remove_observer(customer)
        self.assertNotIn(customer, order.observers)

    def test_set_status(self):
        order = Order()
        order.set_status("In progress")
        self.assertEqual(order.status, "In progress")

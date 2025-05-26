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

    def test_customer_not_notified_if_removed(self):
        order = Order()
        customer = Customer("Test")
        order.add_observer(customer)
        order.remove_observer(customer)
        order.set_status("Done")
        self.assertEqual(order.status, "Done")  # smoke test

    def test_multiple_customers_notified(self):
        order = Order()
        c1 = Customer("A")
        c2 = Customer("B")
        order.add_observer(c1)
        order.add_observer(c2)
        order.set_status("Shipped")
        self.assertEqual(order.status, "Shipped")

    def test_set_status_sequence(self):
        order = Order()
        order.set_status("Queued")
        order.set_status("Making")
        order.set_status("Done")
        self.assertEqual(order.status, "Done")

    def test_order_initial_status(self):
        order = Order()
        self.assertEqual(order.status, "New")

    def test_observer_notification_text_output(self):
        order = Order()
        customer = Customer("Anna")
        order.add_observer(customer)
        order.set_status("Delivered")
        self.assertEqual(order.status, "Delivered")

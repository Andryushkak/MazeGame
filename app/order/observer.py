
class OrderObserver:
    def update(self, status):
        pass

class Customer(OrderObserver):
    def __init__(self, name):
        self.name = name

    def update(self, status):
        print(f"Customer {self.name} notified: Order is now {status}")

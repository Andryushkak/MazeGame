
class Order:
    def __init__(self):
        self.status = "New"
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def set_status(self, status):
        self.status = status
        self.notify_observers()

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.status)

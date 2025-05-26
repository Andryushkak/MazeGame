
from .base import Espresso, Latte, Cappuccino

class CoffeeFactory:
    def create_coffee(self, type_name):
        if type_name == "Espresso":
            return Espresso()
        elif type_name == "Latte":
            return Latte()
        elif type_name == "Cappuccino":
            return Cappuccino()
        else:
            raise ValueError("Unknown coffee type")

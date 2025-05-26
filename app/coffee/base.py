
class Coffee:
    def __init__(self):
        self.description = "Unknown Coffee"

    def get_description(self):
        return self.description

    def cost(self):
        return 0.0

class Espresso(Coffee):
    def __init__(self):
        super().__init__()
        self.description = "Espresso"

    def cost(self):
        return 1.5

class Latte(Coffee):
    def __init__(self):
        super().__init__()
        self.description = "Latte"

    def cost(self):
        return 2.0

class Cappuccino(Coffee):
    def __init__(self):
        super().__init__()
        self.description = "Cappuccino"

    def cost(self):
        return 2.5

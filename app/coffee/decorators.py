
class IngredientDecorator:
    def __init__(self, coffee):
        self.coffee = coffee

    def get_description(self):
        return self.coffee.get_description()

    def cost(self):
        return self.coffee.cost()

class Milk(IngredientDecorator):
    def get_description(self):
        return self.coffee.get_description() + ", Milk"

    def cost(self):
        return self.coffee.cost() + 0.3

class Chocolate(IngredientDecorator):
    def get_description(self):
        return self.coffee.get_description() + ", Chocolate"

    def cost(self):
        return self.coffee.cost() + 0.5

class Syrup(IngredientDecorator):
    def get_description(self):
        return self.coffee.get_description() + ", Syrup"

    def cost(self):
        return self.coffee.cost() + 0.5

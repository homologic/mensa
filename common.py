# Common classes and methods.

class Food :
    def __init__(self,name, price="", category=None, veggie=False) :
        self.name = name
        self.price = price
        self.category = category
        self.veggie = veggie

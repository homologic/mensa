# Common classes and methods.

class Food :
    def __init__(self,name, price="", category="Essen", veggie=False, desc=None) :
        self.name = name
        self.price = price
        self.category = category
        self.veggie = veggie
        self.desc=desc

def formt (food) :
    cat = []
    vegkeys = [ "", "Vegetarian", "Vegan" ]
    r = ""
    food.sort(key=lambda foo: foo.category)
    for i in food:
        if not i.category in cat :
            cat.append(i.category)
            if not i.category == None : 
                r=r+ i.category+"\n"
        r=r+"\t" + i.name.ljust(80) + "\t"+ i.price.ljust(20) + vegkeys[i.veggie]+"\n"
        if i.desc :
            r = r+"\t  "+i.desc+"\n"
    return r

foodsources = {}

class Foodsource :
    def __init__(self, name, function, args):
        pass

def register_foodsource():
    pass

# Common classes and methods.

class Food :
    def __init__(self,name, price="", category="Essen", veggie=False, desc=None, ingredients={}) :
        self.name = name
        self.price = price
        self.category = category
        self.veggie = veggie
        self.desc=desc
        self.ingredients=ingredients
        
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

class Restaurant(object):
    def __init__(self, name, human_name, module, optional_args=[], obligatory_args=()):
        self.name = name
        self.human_name = human_name
        self.module = module
        self.optional_args = optional_args
        self.obligatory_args = obligatory_args

    def get_food(**opt_args) :
        self.module.get_food_items(*obligatory_args, **optional_args)


def register_restaurant(restaurant):
    global foodsources
    foodsources[restaurant.name] = (restaurant)

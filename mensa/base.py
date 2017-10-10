# This file contains functions and classes necessary for the operation of backends.

class Food :
    def __init__(self,name, price="", category="Essen", veggie=False, desc=None, ingredients={}) :
        self.name = name
        self.price = price
        self.category = category
        self.veggie = veggie
        self.desc=desc
        self.ingredients=ingredients

class NoMenuError(Exception) :
    """ gets raised if there's no menu"""

class Renderer(object) :
    def __init__(self, name, human_name, module, description="", optional_args=[]) :
        self.name = name
        self.human_name = human_name
        self.description = description
        self.optional_args = []
        self.module = module
    def render(self, foods, **options) :
        self.module.render(foods, **options)
        
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
renderers = {}

class Restaurant(object):
    def __init__(self, name, human_name, module, optional_args=[], obligatory_args=()):
        self.name = name
        self.human_name = human_name
        self.module = module
        self.optional_args = optional_args
        self.obligatory_args = obligatory_args

    def get_food(self,**opt_args) :
        return self.module.get_food_items(*self.obligatory_args, **opt_args)

def register_restaurant(restaurant):
    global foodsources
    foodsources[restaurant.name] = restaurant
def register_renderer(renderer) :
    global renderers
    renderers[renderer.name] = renderer

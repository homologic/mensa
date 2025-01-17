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
        
from math import acos, radians, pi, cos, sin
def dist(pos1, pos2) :
    # gives a rough estimate of the distance Accuracy: +/- cos(angle
    # between coordinates)*37/2pi. (about +/- 50 m for distances).
    # Distance is returned in km
    if pos1 is None or pos2 is None :
        return float("Inf")
    lat1, long1 = pos1
    lat2, long2 = pos2

    a = radians(90 - lat1);
    b = radians(90 - lat2);
    C = radians(abs(long1-long2));
    return acos(cos(a)*cos(b)+sin(a)*sin(b)*cos(C))*40040/(2*pi);


foodsources = {}
renderers = {}

class Restaurant(object):
    def __init__(self, name, human_name, module, optional_args=[], obligatory_args=(), pos=None):
        self.name = name
        self.human_name = human_name
        self.module = module
        self.optional_args = optional_args
        self.obligatory_args = obligatory_args
        self.pos = pos

    def get_food(self,**opt_args) :
        return self.module.get_food_items(*self.obligatory_args, **opt_args)


def register_restaurant(restaurant):
    global foodsources
    foodsources[restaurant.name] = restaurant
def register_renderer(renderer) :
    global renderers
    renderers[renderer.name] = renderer

def only_student_prices(price):
    return price.split("/")[0]

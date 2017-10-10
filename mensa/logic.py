#!/usr/bin/python3

from mensa import base
import urllib.error
import os
from yapsy.PluginManager import PluginManager

def init_foodsources():
    backends = PluginManager()
    backends.setPluginPlaces([os.path.join(os.path.dirname(os.path.realpath(__file__)),"backends")])    
    backends.collectPlugins()
    for pluginInfo in backends.getAllPlugins():
        backends.activatePluginByName(pluginInfo.name)
        pluginInfo.plugin_object.register_restaurants()

def init_renderers():
    frontends = PluginManager()
    frontends.setPluginPlaces([os.path.join(os.path.dirname(os.path.realpath(__file__)),"frontends")])
    frontends.collectPlugins()
    for pluginInfo in frontends.getAllPlugins():
        frontends.activatePluginByName(pluginInfo.name)
        pluginInfo.plugin_object.register_renderer()
    
    
def get_food(restlist=False, options={}) :
    foodl = []
    for k,i in base.foodsources.items() :
        if restlist and not i.name in restlist :
            continue
        try : 
            food = i.get_food(ignore_nudelauswahl=True)
            foodl.append((i, food))
            # print("*"*20+i.human_name+"*"*20+"\n"+base.formt(food))
        except base.NoMenuError:
            print(i.human_name + ": No menu found. This could be due to a holiday or due to an error in the script.")
        except urllib.error.HTTPError as e :
            print(i.human_name + ": Fetching menu failed: %s" % str(e))
    return foodl

def render(to_render, rendlist=False, options={}) :
    for k,i in base.renderers.items() :
        if rendlist and not i.name in rendlist :
            continue
        i.render(to_render)

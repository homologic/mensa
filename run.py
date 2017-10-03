#!/usr/bin/python3
from yapsy.PluginManager import PluginManager
backends = PluginManager()
backends.setPluginPlaces(["./backends"])
backends.collectPlugins()
import base
for pluginInfo in backends.getAllPlugins():
    backends.activatePluginByName(pluginInfo.name)
    pluginInfo.plugin_object.register_restaurants()

for k,i in base.foodsources.items() :
    try : 
        food = i.get_food()
        print("*"*20+i.human_name+"*"*20+"\n"+base.formt(food))
    except base.NoMenuError:
        print(i.human_name + ": No menu found. This could be due to a holiday or due to an error in the script.")

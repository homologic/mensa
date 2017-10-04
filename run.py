#!/usr/bin/python3

import base

import argparse

parser = argparse.ArgumentParser(description='Fetch menus from various sources')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
parser.add_argument('-r', '--restaurants',  dest='rest', action='store',
                    metavar='LIST',
                    help='Comma-separated list of restaurants to fetch the menus from.')
parser.add_argument('-l', '--list-restaurants',  dest='list', action='store_true',
                    help='get list of restaurants')


args = parser.parse_args()
## Load backends
from yapsy.PluginManager import PluginManager
backends = PluginManager()
backends.setPluginPlaces(["./backends"])
backends.collectPlugins()
## Load frontends (not yet implemented)
# from yapsy.PluginManager import PluginManager
# frontends = PluginManager()
# frontends.setPluginPlaces(["./frontends"])
# frontends.collectPlugins()

for pluginInfo in backends.getAllPlugins():
    backends.activatePluginByName(pluginInfo.name)
    pluginInfo.plugin_object.register_restaurants()

if args.list :
    for k,i in base.foodsources.items():
        print(i.name, i.human_name)
    exit()
restlist = None
if args.rest :
    restlist = args.rest.split(",")
    
for k,i in base.foodsources.items() :
    if restlist and not i.name in restlist :
        continue
    try : 
        food = i.get_food(ignore_nudelauswahl=True)
        print("*"*20+i.human_name+"*"*20+"\n"+base.formt(food))
    except base.NoMenuError:
        print(i.human_name + ": No menu found. This could be due to a holiday or due to an error in the script.")
    except urllib.error.HTTPError as e :
        print(i.human_name + ": Fetching menu failed: %s" % str(e))

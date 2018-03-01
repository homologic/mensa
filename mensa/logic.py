#!/usr/bin/python3

from mensa import base
import urllib.error
import os
import sys
from yapsy.PluginManager import PluginManager
try:
    import multiprocessing
    parallel=True
except:
    parallel = False

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
    
    
def get_food(restlist=False, **options) :
    foodl = []
    if parallel :
        r = []
        for k,i in base.foodsources.items() :
            if restlist and not i.name in restlist :
                continue
            r.append(i)
            
        foodl = get_food_parallel(r, ignore_nudelauswahl=True)
    else : 
        for k,i in base.foodsources.items() :
            if restlist and not i.name in restlist :
                continue
            try : 
                food = i.get_food(ignore_nudelauswahl=True)
                foodl.append((i, food))
                # print("*"*20+i.human_name+"*"*20+"\n"+base.formt(food))
            except base.NoMenuError:
                sys.stderr.write(i.human_name + ": No menu found. This could be due to a holiday or due to an error in the script.\n")
            except urllib.error.HTTPError as e :
                sys.stderr.write(i.human_name + ": Fetching menu failed: %s\n" % str(e))
            except :
                sys.stderr.write(i.human_name + ": Unknown error\n")
    return foodl

# format:
# if __name__ == "__main__":
#     pool = multiprocessing.Pool(4)
#     k = pool.map(pr_f, list(mensenliste.items()))
#     k.sort(key=lambda x: x[0])
#     for i in k :
#         print(i[1])
def get_food_parallel_helper(i) :
    try : 
        return (i[0],i[0].get_food(**i[1]))
    except:
        sys.stderr.write(i[0].human_name + ": No menu found. This could be due to a holiday or due to an error in the script.\n")
        return (i[0], [])

def get_food_parallel(rl, **options) :
    pool = multiprocessing.Pool(60)
    k = [ (i, options) for i in rl ]
    l = list(pool.map(get_food_parallel_helper, k))
    l.sort(key=lambda x: x[0].human_name)
    return l

def render(to_render, rendlist=False, **options) :
    for k,i in base.renderers.items() :
        if rendlist and not i.name in rendlist :
            continue
        i.render(to_render, **options)

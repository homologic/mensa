# Copyright (C) 2017 Antonia Perez-Cerezo <antonia@antonia.is>
# -*- coding: utf-8 -*-

import urllib.request, urllib.error, urllib.parse
from lxml import etree
from lxml.cssselect import CSSSelector
import html5lib
from mensa.base import *
from yapsy.IPlugin import IPlugin
import multiprocessing


from yapsy import NormalizePluginNameForModuleName as normalize

mensenliste = {"TU Hardenbergstraße" : "mensa-tu-hardenbergstra%C3%9Fe", "TU Marchstraße": "cafeteria-tu-marchstra%C3%9Fe", "TU Skyline": "cafeteria-tu-skyline", "TU Architektur": "cafeteria-tu-architektur", "TU Ackerstraße": "cafeteria-tu-ackerstra%C3%9Fe"}



def pr_f(j) :
    i,k = j
    food = get_food_items(k, ignore_nudelauswahl=True)
    return (i,"*"*20+i+"*"*20+"\n"+formt(food))

class Studentenwerk(IPlugin) :
    def register_restaurants (self) :
        mensenliste = {"TU Hardenbergstraße" : "mensa-tu-hardenbergstra%C3%9Fe", "TU Marchstraße": "cafeteria-tu-marchstra%C3%9Fe", "TU Skyline": "cafeteria-tu-skyline", "TU Architektur": "cafeteria-tu-architektur", "TU Ackerstraße": "cafeteria-tu-ackerstra%C3%9Fe"}
        for h,n in mensenliste.items() :
            r = Restaurant(normalize(h), h, self, "dummy", [n])
            register_restaurant(r)
    def get_food_items(self, mensa="mensa-tu-hardenbergstra%C3%9Fe", ignore_nudelauswahl=False) :
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}
        
        req = urllib.request.Request('https://www.stw.berlin/mensen/%s.html' % mensa, headers=headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        document = html5lib.parse(the_page, treebuilder="lxml")
        groupsel = CSSSelector('.splGroupWrapper')
        groups = [e for e in groupsel(document)]
        fl = []
        for i in groups :
            try: 
                name = CSSSelector('.splGroup')(i)[0].text
            except:
                raise NoMenuError from None
            sel = CSSSelector('.splMeal')
            meals = [e for e in sel(i)]
            for m in meals :        
                namesel = CSSSelector('.bold')
                nm = namesel(m)[0].text
                if ignore_nudelauswahl  and "Nudelauswahl" in nm :
                    continue
                pricesel = CSSSelector('.col-md-3')
                veg = 0
                if len(pricesel(m)[0]) >= 2 :
                    if "15" in pricesel(m)[0][1].attrib["src"] :
                        veg = 2
                    elif "1.png" in pricesel(m)[0][1].attrib["src"] :
                        veg = 1
                price = pricesel(m)[-1].text.strip()
                fl.append(Food(nm, price, name, veg))
        return fl



# format:
# if __name__ == "__main__":
#     pool = multiprocessing.Pool(4)
#     k = pool.map(pr_f, list(mensenliste.items()))
#     k.sort(key=lambda x: x[0])
#     for i in k :
#         print(i[1])

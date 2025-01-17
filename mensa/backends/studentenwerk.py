# Copyright (C) 2017 Antonia Perez-Cerezo <antonia@antonia.is>
# -*- coding: utf-8 -*-

import urllib.request, urllib.error, urllib.parse
from lxml import etree
from lxml.cssselect import CSSSelector
import html5lib
from mensa.base import *
from yapsy.IPlugin import IPlugin
import multiprocessing
import datetime
from collections import OrderedDict

boring = ["Desserts", "Salate"] # categories which are considered boring because they contain the same food every day.

from yapsy import NormalizePluginNameForModuleName as normalize
mensenliste = {"TU Hardenbergstraße" : ["mensa-tu-hardenbergstra%C3%9Fe", (52.5097684, 13.3259478)],
               "TU Veggie 2.0" : ["veggie2.0", (52.5097684, 13.3259478)],
               "TU Marchstraße": ["cafeteria-tu-marchstra%C3%9Fe", ( 52.5166071, 13.3234066)],
               "TU Skyline": ["einrichtungen/technische-universit%C3%A4t-berlin/mensa-tu-skyline", (52.5128648, 13.3200313)],
               "TU Architektur": ["cafeteria-tu-architektur", (52.5137508, 13.3234541)],
               "TU Ackerstraße": ["cafeteria-tu-ackerstra%C3%9Fe", (52.5386545, 13.3845294)],
               "HU Nord": ["mensa-hu-nord", (52.52816,13.38208)],
               "HU Oase Adlershof" : ["mensa-hu-oase-adlershof", ( 52.4293965, 13.5300404)],
               "HU Süd": ["mensa-hu-sued", (52.5185929, 13.3928965)],
               "HU Spandauer Straße": ["mensa-hu-spandauer-stra%C3%9Fe", (52.52096,13.40258)],
               "HU „Jacob und Wilhelm Grimm Zentrum“": ["cafeteria-hu-im-jacob-und-wilhelm-grimm-zentrum", (52.52033,13.39083)],
               "FU Herrenhaus Düppel": ["mensa-fu-herrenhaus-d%C3%BCppel", (52.4299794,13.2352233)],
               "Mensa FU II Otto-von-Simson-Straße": ["mensa-fu-ii", (52.4531000, 13.2890712)],               
}



class Studentenwerk(IPlugin) :
    def fetch_page(self, mensa) :
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}
        
        req = urllib.request.Request('https://www.stw.berlin/mensen/%s.html' % mensa, headers=headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        open("/tmp/the_page","w").write(str(the_page))
        document = html5lib.parse(the_page, treebuilder="lxml")
        return document
    def register_restaurants (self) :
        for h,n in mensenliste.items() :
            r = Restaurant(normalize(h), h, self, "dummy", [n[0]], pos=n[1])
            register_restaurant(r)
    def get_food_items(self, mensa="mensa-tu-hardenbergstra%C3%9Fe", **options) :
        document = self.fetch_page(mensa)
        groupsel = CSSSelector('.splGroupWrapper')
        groups = [e for e in groupsel(document)]
        fl = OrderedDict()
        no_boring = False 
        if "args" in options : 
            no_boring = options["args"].no_boring
        for group in groups :
            try:
                category = CSSSelector('.splGroup')(group)[0].text
            except:
                continue
                #raise NoMenuError from None
            if no_boring and category in boring :
                continue
            if category == "Aktionen" : # remove arbitrary distinction between meal types.
                category = "Essen"
            if category == "Suppen" or category == "Vorspeisen" :
                category = "Suppen und Vorspeisen"
            if not category in fl :
                fl[category] = []
            sel = CSSSelector('.splMeal')
            meals = [e for e in sel(group)]
            for m in meals :        
                namesel = CSSSelector('.bold')
                nm = namesel(m)[0].text.strip()
                if no_boring  and ( "Nudelauswahl" in nm or nm in ["Hartkäse gerieben", "Sauce & Dip Extra"] ):
                    continue
                pricesel = CSSSelector('.col-md-3')
                veg = 0
                if len(pricesel(m)[0]) >= 2 :
                    for k in pricesel(m)[0]:
                        if "src" in k.attrib :
                            if "15" in k.attrib["src"] :
                                veg = 2
                            elif "1.png" in k.attrib["src"] :
                                veg = 1
                price = pricesel(m)[-1].text.strip()
                if "only_student_prices" in options and options["only_student_prices"] :
                    price = only_student_prices(price)
                fl[category].append(Food(nm, price, category, veg))
        return fl
    def get_opening_hours(self, mensa) :
        #### Rudiment of a function for getting opening hours. Does NOT work yet due to unknown issues.
        doc = self.fetch_page(mensa)
        groupsel = CSSSelector('div.col-xs-10')
        groups = [e for e in groupsel(doc)]
        print(groups)
        return doc


# format:
# if __name__ == "__main__":
#     pool = multiprocessing.Pool(4)
#     k = pool.map(pr_f, list(mensenliste.items()))
#     k.sort(key=lambda x: x[0])
#     for i in k :
#         print(i[1])

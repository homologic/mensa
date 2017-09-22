# Copyright (C) 2017 Antonia Perez-Cerezo <antonia@antonia.is>

import urllib2
from lxml import etree
from lxml.cssselect import CSSSelector
import html5lib
from common import Food

def get_food_items(mensa="mensa-tu-hardenbergstra%C3%9Fe", ignore_nudelauswahl=False) :
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    
    req = urllib2.Request('https://www.stw.berlin/mensen/mensa-tu-hardenbergstra%C3%9Fe.html', headers=headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    document = html5lib.parse(the_page, treebuilder="lxml")
    groupsel = CSSSelector('.splGroupWrapper')
    groups = [e for e in groupsel(document)]
    fl = []
    for i in groups :
        name = CSSSelector('.splGroup')(i)[0].text
        sel = CSSSelector('.splMeal')
        meals = [e for e in sel(i)]
        for m in meals :        
            namesel = CSSSelector('.bold')
            nm = namesel(m)[0].text
            if ignore_nudelauswahl  and "Nudelauswahl" in nm:
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
if __name__ == "__main__":
    food = get_food_items("", ignore_nudelauswahl=True)
    cat = []
    vegkeys = [ "", "Vegetarian", "Vegan" ]
    for i in food:
        if not i.category in cat :
            cat.append(i.category)
            if not i.category == None : 
                print i.category
        print "\t" + i.name.ljust(80) + "\t"+ i.price.ljust(20) + vegkeys[i.veggie]

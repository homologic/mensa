# -*- coding: utf-8 -*-

import urllib.request, urllib.error, urllib.parse
from lxml import etree
from lxml.cssselect import CSSSelector

import  xml.sax.saxutils as saxutils
import html5lib
import datetime
from common import Food
from common import formt

def get_food_items() :
    weekday = datetime.datetime.today().weekday()
    if weekday > 4 :
        print("Error: No food today")
        return ""
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    
    req = urllib.request.Request('http://personalkantine.personalabteilung.tu-berlin.de/', headers=headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    document = html5lib.parse(the_page, treebuilder="lxml")
    sel = CSSSelector('.Menu__accordion')
    fl = []
    for k in sel(document)[0][weekday] :
        if k.tag.endswith("ul") :
            for j in k :
                price = j[1].text
                st = str(etree.tostring(j)).split("\\n")[2].split("<")[0]
                name = j[0].text + ", " + etree.fromstring("<p>%s</p>"%st).text.strip() # really extremely dirty hack
                veg = 0
                if "(v)" in name or "Gemüseplatte" in name :
                    veg = 1
                fl.append(Food(name, price, "Menü", veg))
    return fl

if __name__ == "__main__":
    food = get_food_items()
    print(formt(food))

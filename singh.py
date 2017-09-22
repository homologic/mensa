import urllib.request, urllib.error, urllib.parse
from lxml import etree
from lxml.cssselect import CSSSelector
import html5lib
from common import Food
from common import formt
import re
import sys
import datetime


def get_food_items() :
    sys.stderr = open("/dev/null", "w")
    weekday = datetime.datetime.today().weekday()
    if weekday > 4 :
        print("Error: No food today")
        return ""
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    
    req = urllib.request.Request('http://singh-catering.de/cafe/', headers=headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    document = html5lib.parse(the_page, treebuilder="lxml")
    groupsel = CSSSelector('.menu-list__items')
    myorder=[0,3,1,4,2]
    mylist = [ groupsel(document)[i] for i in myorder]
    i = mylist[weekday]
    fl = []
    nmsel = CSSSelector('.menu-list__item')
    for k in nmsel(i):
        veg = 0
        titsel = CSSSelector('.item_title')
        name = titsel(k)[0].text
        dscsel = CSSSelector('.desc__content')
        desc = dscsel(k)[0].text
        prsel = CSSSelector('.menu-list__item-price')
        price = prsel(k)[0].text
        vegsel = CSSSelector('.menu-list__item-highlight-title')
        if len(vegsel(k)) > 0 :
            if "VEGETARISCH" in vegsel(k)[0].text :
                veg = 1
            elif "VEGAN" in vegsel(k)[0].text :
                veg = 2
        fl.append(Food(name, price, "Essen", veg, desc))
    return fl
                    
if __name__ == "__main__":
    food = get_food_items()
    print(formt(food))


import urllib.request, urllib.error, urllib.parse
from lxml import etree
from lxml.cssselect import CSSSelector
import html5lib
from mensa.base import *
import re
import sys
from yapsy.IPlugin import IPlugin

class Satyam(IPlugin):
    def register_restaurants(self) :
        r = Restaurant("Satyam", "Satyam", self, "dummy")
        register_restaurant(r)
    def get_food_items(self, **kwargs) :
        s = sys.stderr
        sys.stderr = open("/dev/null", "w")
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}

        req = urllib.request.Request('http://www.mysatyam.de/angebote/express-mittagstisch.html', headers=headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        document = html5lib.parse(the_page, treebuilder="lxml")
        sys.stderr = s
        groupsel = CSSSelector('.news-latest-item-content')
        k = etree.tostring(groupsel(document)[0])
        price = groupsel(document)[0][-1].text.strip()
        name = re.sub(r'<.+?>', ' ', str(k))
        name = etree.fromstring("<p>%s</p>"%name).text.strip()
        name = name.replace("\\n", "")
        name = " ".join(name.split())
        name = name.replace(price, "")

        return [Food("Mittagstisch Express", price, "Mittagstisch", 2, name[3:-1])]
    

# if __name__ == "__main__":
#     food = get_food_items()
#     print(formt(food))

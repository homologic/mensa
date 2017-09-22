import urllib.request, urllib.error, urllib.parse
from lxml import etree
from lxml.cssselect import CSSSelector
import html5lib
from common import Food
from common import formt
import re
import sys


def get_food_items() :
    sys.stderr = open("/dev/null", "w")
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    
    req = urllib.request.Request('http://www.mysatyam.de/angebote/express-mittagstisch.html', headers=headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    document = html5lib.parse(the_page, treebuilder="lxml")
    groupsel = CSSSelector('.news-latest-item-content')
    k = etree.tostring(groupsel(document)[0])
    name = re.sub(r'<.+?>', ' ', str(k))
    name = etree.fromstring("<p>%s</p>"%name).text.strip()
    name = name.replace("\\n", "")
    name = " ".join(name.split())

    name = name.replace("5,95 €", "")
#    print(name[3:-1])
    return [Food("Mittagstisch Express", "5,95 €", "Mittagstisch", 2, name[3:-1])]
    

if __name__ == "__main__":
    food = get_food_items()
    print(formt(food))

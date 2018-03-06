from mensa import base
from yapsy.IPlugin import IPlugin
from  xml.sax.saxutils import escape as esc

class HTMLRenderer(IPlugin) :
    def render (self, foods, **options) :
        ## Expects list of tuples with (Restaurant, Foodlist)
        r = ""
        vegkeys = [ "", "Vegetarian", "Vegan" ]
        for restaurant, food in foods :
            cat = []
            if not food :
                continue
            r = r+"<div class=\"restaurant\"><h3>"+esc(restaurant.human_name)+"</h3>"+"\n"#+base.formt(food)
            food.sort(key=lambda foo: foo.category)
            for i in food:
                if options["only_student_prices"] :
                    price = base.only_student_prices(i.price)
                else:
                    price = i.price
                if options["only_veggie"] and options["only_veggie"] > i.veggie :
                    continue
                if not i.category in cat :
                    if cat :
                        r = r + "</ul>"
                    cat.append(i.category)
                    if not i.category == None : 
                        r=r+ "<h4>"+esc(i.category)+"</h4><ul class=\"food-by-cat\">\n"
                r=r+"<li class=\"fooditem\" ><span class=\"name\">" + esc(i.name) + "</span><span class=\"price\">"+ esc(price) + "</span><span class=\"veggie\">"+ esc(vegkeys[i.veggie])+"</span>\n"
                if i.desc :
                    r = r+"<div class=\"description\">"+esc(i.desc)+"</div>\n"
            r = r+"</div>"
        r = r
        print(r)

    def register_renderer(self) :
        base.register_renderer(base.Renderer("html", "HTML Renderer", self))

from mensa import base
from yapsy.IPlugin import IPlugin
class TextRenderer(IPlugin) :
    def render (self, foods, **options) :
        ## Expects list of tuples with (Restaurant, Foodlist)
        r = ""
        vegkeys = [ "", "Vegetarian", "Vegan" ]
        for restaurant, food in foods :
            cat = []
            if not food :
                continue
            r = r+"*"*20+restaurant.human_name+"*"*20+"\n"#+base.formt(food)
            food.sort(key=lambda foo: foo.category)
            for i in food:
                if options["only_student_prices"] :
                    price = base.only_student_prices(i.price)
                else:
                    price = i.price
                if options["only_veggie"] and options["only_veggie"] > i.veggie :
                    continue
                if not i.category in cat :
                    cat.append(i.category)
                    if not i.category == None : 
                        r=r+ i.category+"\n"
                r=r+"\t" + i.name.ljust(80) + "\t"+ price.ljust(20) + vegkeys[i.veggie]+"\n"
                if i.desc :
                    r = r+"\t  "+i.desc+"\n"
        print(r)

    def register_renderer(self) :
        base.register_renderer(base.Renderer("plain-text", "Plain Text Renderer", self))

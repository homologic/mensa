import base
from yapsy.IPlugin import IPlugin
class TextRenderer(IPlugin) :
    def render (self, foods, **options) :
        ## Expects list of tuples with (Restaurant, Foodlist)
        r = ""
        vegkeys = [ "", "Vegetarian", "Vegan" ]
        for restaurant, food in foods :
            cat = []
            r = r+"*"*20+restaurant.human_name+"*"*20+"\n"#+base.formt(food)
            food.sort(key=lambda foo: foo.category)
            for i in food:
                if not i.category in cat :
                    cat.append(i.category)
                    if not i.category == None : 
                        r=r+ i.category+"\n"
                r=r+"\t" + i.name.ljust(80) + "\t"+ i.price.ljust(20) + vegkeys[i.veggie]+"\n"
                if i.desc :
                    r = r+"\t  "+i.desc+"\n"
        print(r)

            

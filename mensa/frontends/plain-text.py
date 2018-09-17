from mensa import base
from yapsy.IPlugin import IPlugin
class TextRenderer(IPlugin) :
    def render_line(self, item) :
        vegkeys = [ "", "Vegetarian", "Vegan" ]
        if self.options.get("only_veggie",0) > item.veggie :
            return ""
        desc = ""
        if item.desc : 
            desc = "\t  "+item.desc+"\n"            
        return "\t" + item.name.ljust(80) + "\t"+ item.price.ljust(20) + vegkeys[item.veggie]+"\n"+desc
    
    def render (self, foods, **options) :
        self.options = options
        ## Expects list of tuples with (Restaurant, Foodlist)
        r = ""
        for restaurant, food in foods :
            cat = []
            if not food :
                continue
            r = r+"*"*20+restaurant.human_name+"*"*20+"\n"
            if "pos" in options and restaurant.pos and options.get("dist") :
                ## display distance to restaurant
                r=r+"Distance: %.2f km\n" % base.dist(options["pos"], restaurant.pos)

            r= r + "".join([category+"\n" + "".join([self.render_line(i) for i in items]) for category,items  in food.items()])

        if options.get("template") :
            f = open(options["template"], "r")
            template = f.read()
            f.close()
            print(template.replace("$$TEXT$$", r))
        else :
            print(r)

    def register_renderer(self) :
        base.register_renderer(base.Renderer("plain-text", "Plain Text Renderer", self))

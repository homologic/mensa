from mensa import base
from yapsy.IPlugin import IPlugin
from  xml.sax.saxutils import escape as esc

class HTMLRenderer(IPlugin) :
    def format_line(self, item) :
        vegkeys = [ "", "Vegetarian", "Vegan" ]
        if self.options.get("only_veggie",0) > item.veggie :
            return ""
        if item.desc :
            desc = "<div class=\"description\">"+esc(item.desc)+"</div>\n"
        else :
            desc = ""
        return"<li class=\"fooditem\" ><span class=\"name\">" + esc(item.name) + "</span><span class=\"price\">"+ esc(item.price) + "</span><span class=\"veggie\">"+ esc(vegkeys[item.veggie])+"</span>\n"+ desc
        
    def format_category(self, category, items) :
        return "<h4>%s</h4></h4><ul class=\"food-by-cat\">\n%s</ul>" % (esc(category), "".join([self.format_line(i) for i in items]))
    def format_restaurant(self, restaurant, food) :
        if not food :
            return ""
        st = "<div class=\"restaurant\"><h3>%s</h3>\n" % esc(restaurant.human_name)
        dist = ""
        if "pos" in self.options and restaurant.pos and self.options.get("dist") :
            dist = "<div class=\"distance\">Distance: %.2f km</div>\n" % base.dist(options["pos"], restaurant.pos)
        body = "\n".join([self.format_category(cat, it) for cat,it in food.items()])
        return st+dist+body+"</div>"
    def render (self, foods, **options) :
        ## Expects list of tuples with (Restaurant, Foodlist)
        self.options = options

        r = "\n".join([self.format_restaurant(restaurant, food) for restaurant, food in foods ])

        print(r)

    def register_renderer(self) :
        base.register_renderer(base.Renderer("html", "HTML Renderer", self))

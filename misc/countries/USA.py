from csdl import *


class USA(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/countries/USA.py")
        self.extendsId = "NorthAmerica"

        self.name = "United States of America"

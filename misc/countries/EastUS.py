from csdl import *


class EastUS(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/countries/EastUS.py")
        self.extendsId = "https://github.com/supermuesli/csdl@misc/countries/USA.py@latest"

        self.name = "East United States of America (USA)"

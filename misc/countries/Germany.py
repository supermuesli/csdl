from csdl import *


class Germany(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/countries/Germany.py")
        self.extendsId = "Europe"

        self.name = "Germany"

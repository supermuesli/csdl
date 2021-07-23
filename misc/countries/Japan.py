from csdl import *


class Japan(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/countries/Japan.py")
        self.extendsId = "EastAsia"

        self.value = "Japan"

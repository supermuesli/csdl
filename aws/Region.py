from csdl import *


class Region(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/Region.py")
        self.extendsId = "Region"

        self.options = ["East Virginia", "New York", "California"]
        self.value = self.options[0]

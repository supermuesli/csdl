from csdl import *


class Currency(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/Currency.py")
        self.extendsId = "ChoiceAttribute"

        self.options = ["us-dollar", "euro", "yen"]
        self.value = self.options[0]

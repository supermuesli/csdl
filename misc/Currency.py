from csdl import *


class Currency(ChoiceAttribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/Currency.py")

        self.value = self.options[0]
        self.options = ["us-dollar", "euro", "yen"]

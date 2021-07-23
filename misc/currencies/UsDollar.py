from csdl import *


class UsDollar(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/currencies/UsDollar.py")
        self.extendsId = "Currency"

        self.value = "New York"

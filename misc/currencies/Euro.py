from csdl import *


class UsDollar(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/currencies/Euro.py")
        self.extendsId = "Currency"

        self.value = "Euro"

from csdl import *


class UsDollar(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/currencies/JapaneseYen.py")
        self.extendsId = "Currency"

        self.value = "Japanese Yen"

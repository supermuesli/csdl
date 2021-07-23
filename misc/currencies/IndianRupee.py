from csdl import *


class IndianRupee(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/currencies/IndianRupee.py")
        self.extendsId = "NameAttribute"

        self.value = "INR"  # https://en.wikipedia.org/wiki/ISO_4217

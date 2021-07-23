from csdl import *


class FeritsCurrencies(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/currencies/FeritsCurrencies.py")
        self.extendsId = "Currency"

        # custom option that I want to add to the existing options
        indianRupee = NameAttribute()
        indianRupee.inject("https://github.com/supermuesli/csdl", "misc/currencies/IndianRupee.py")

        # add my custom option to the already existing options
        self.options = Currency().options + [indianRupee]
        self.value = None

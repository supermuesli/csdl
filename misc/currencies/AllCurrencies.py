from csdl import *


class AllCurrencies(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/currencies/AllCurrencies.py")
        self.extendsId = "Currency"

        # custom option that I want to add to the existing options
        indianRupee = NameAttribute()
        indianRupee.inject("https://github.com/supermuesli/csdl", "misc/currencies/IndianRupee.py")

        # add my custom option to the already existing options
        self.options = Currency().options
        self.options["INR"] = indianRupee
        self.choice = None

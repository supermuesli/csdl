from csdl import *


class Region(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/regions/Region.py")
        self.extendsId = "Region"

        # custom options that I want to add to the existing options
        california = NameAttribute()
        california.inject("https://github.com/supermuesli/csdl", "aws/regions/California.py")

        eastVirginia = NameAttribute()
        eastVirginia.inject("https://github.com/supermuesli/csdl", "aws/regions/EastVirginia.py")

        newYork = NameAttribute()
        newYork.inject("https://github.com/supermuesli/csdl", "aws/regions/NewYork.py")

        # add my custom option to the already existing options
        self.options = Region().options + [california, eastVirginia, newYork]
        self.value = None

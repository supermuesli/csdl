from csdl import *


class Out(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/dataTransfer/Out.py")
        self.extendsId = "NumericAttribute"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.stepSize = 1
        self.moreIsBetter = True

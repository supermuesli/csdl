from csdl import *


class Standard(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/s3/Standard.py")
        self.extendsId = "OptionAttribute"

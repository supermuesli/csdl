from csdl import *


class StandardInfreqAccess(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/s3/StandardInfreqAccess.py")
        self.extendsId = "OptionAttribute"

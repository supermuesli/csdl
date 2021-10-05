from csdl import *


class SingleAZ(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/rdsPostgres/SingleAZ.py")
        self.extendsId = "OptionAttribute"

from csdl import *


class MultiAZ(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/rdsPostgres/MultiAZ.py")
        self.extendsId = "OptionAttribute"

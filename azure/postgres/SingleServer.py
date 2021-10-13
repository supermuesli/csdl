from csdl import *


class SingleServer(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "azure/postgres/SingleServer.py")
        self.extendsId = "OptionAttribute"

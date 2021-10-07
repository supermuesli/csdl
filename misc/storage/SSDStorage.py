from csdl import *


class SSDStorage(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/storage/SSDStorage.py")
        self.extendsId = "Storage"

from csdl import *


class MagneticStorage(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/storage/MagneticStorage.py")
        self.extendsId = "Storage"

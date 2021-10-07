from csdl import *


class IOPSMagneticStorage(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/storage/IOPSMagneticStorage.py")
        self.extendsId = "https://github.com/supermuesli/csdl@misc/storage/MagneticStorage.py@latest"

        self.iops = Attribute()
        self.iops.inject("https://github.com/supermuesli/csdl@misc/dataTransfer/IOPS.py@latest")

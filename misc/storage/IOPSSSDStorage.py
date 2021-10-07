from csdl import *


class IOPSSSDStorage(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/storage/IOPSSSDStorage.py")
        self.extendsId = "https://github.com/supermuesli/csdl@misc/storage/SSDStorage.py@latest"

        self.iops = Attribute()
        self.iops.inject("https://github.com/supermuesli/csdl@misc/dataTransfer/IOPS.py@latest")

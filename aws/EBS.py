from csdl import *


class EBS(StorageAsAService):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/EBS.py")

        self.storageReadSpeed.value = 1000
        self.storageReadSpeed.mutable = False

        self.storageWriteSpeed.value = 500
        self.storageWriteSpeed.mutable = False

        self.storage.makeInt = True
        self.storage.minVal = 100
        self.storage.maxVal = 10000
        self.storage.mutable = True

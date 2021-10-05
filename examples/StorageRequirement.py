from csdl import *


class StorageRequirement(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/StorageRequirement.py")
        self.extendsId = "StorageAsAService"

        self.storage.value = 5000

        self.region.inject("https://github.com/supermuesli/csdl", "aws/regions/Region.py")
        self.region.value = "northernVirginia"

        self.transferIn = Attribute()
        self.transferIn.inject("https://github.com/supermuesli/csdl", "misc/dataTransfer/In.py")
        self.transferIn.value = 10

        self.transferOut = Attribute()
        self.transferOut.inject("https://github.com/supermuesli/csdl", "misc/dataTransfer/Out.py")
        self.transferOut.value = 10000000

from csdl import *


class StorageRequirement(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/StorageRequirement.py")
        self.extendsId = "StorageAsAService"

        self.storage.value = 5000

        self.region.inject("https://github.com/supermuesli/csdl", "aws/regions/Regions.py")
        self.region.value = "northernVirignia"


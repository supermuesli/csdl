from csdl import *


class StorageRequirement(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/StorageRequirement.py")
        self.extendsId = "StorageAsAService"

        self.storage.value = 5000

        usa = Attribute()
        usa.inject("https://github.com/supermuesli/csdl", "misc/countries/USA.py")
        self.region.options.update({
            "usa": usa
        })
        self.region.value = "usa"

        self.transferOut = Attribute()
        self.transferOut.inject("https://github.com/supermuesli/csdl", "misc/dataTransfer/Out.py")
        self.transferOut.value = 10000

        self.getAmount = Attribute()
        self.getAmount.inject("https://github.com/supermuesli/csdl", "misc/requests/GETAmount.py")
        self.getAmount.value = 13000

        self.postAmount = Attribute()
        self.postAmount.inject("https://github.com/supermuesli/csdl", "misc/requests/POSTAmount.py")
        self.postAmount.value = 10420

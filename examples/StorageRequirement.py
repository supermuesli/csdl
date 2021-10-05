from csdl import *


class StorageRequirement(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/StorageRequirement.py")
        self.extendsId = "StorageAsAService"

        self.storage.value = 5000

        awsRegions = Attribute()
        awsRegions.inject("https://github.com/supermuesli/csdl", "aws/regions/Region.py")
        self.region.options.update(awsRegions.options)
        self.region.value = "northernVirginia"

        self.transferIn = Attribute()
        self.transferIn.inject("https://github.com/supermuesli/csdl", "misc/dataTransfer/In.py")
        self.transferIn.value = 10

        self.transferOut = Attribute()
        self.transferOut.inject("https://github.com/supermuesli/csdl", "misc/dataTransfer/Out.py")
        self.transferOut.value = 10000000

        self.s3type = Attribute()
        self.s3type.inject("https://github.com/supermuesli/csdl", "aws/s3/S3Type.py")
        self.s3type.value = "standard"

        self.putAmount = Attribute()
        self.putAmount.inject("https://github.com/supermuesli/csdl", "misc/requests/PUTAmount.py")
        self.putAmount.value = 600

        self.copyAmount = Attribute()
        self.copyAmount.inject("https://github.com/supermuesli/csdl", "misc/requests/COPYAmount.py")
        self.copyAmount.value = 202

        self.listAmount = Attribute()
        self.listAmount.inject("https://github.com/supermuesli/csdl", "misc/requests/LISTAmount.py")
        self.listAmount.value = 900

        self.getAmount = Attribute()
        self.getAmount.inject("https://github.com/supermuesli/csdl", "misc/requests/GETAmount.py")
        self.getAmount.value = 13000

        self.selectAmount = Attribute()
        self.selectAmount.inject("https://github.com/supermuesli/csdl", "misc/requests/SELECTAmount.py")
        self.selectAmount.value = 42

        self.postAmount = Attribute()
        self.postAmount.inject("https://github.com/supermuesli/csdl", "misc/requests/POSTAmount.py")
        self.postAmount.value = 10420

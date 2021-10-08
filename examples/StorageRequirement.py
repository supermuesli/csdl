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

        self.transferOut = Attribute()
        self.transferOut.inject("https://github.com/supermuesli/csdl", "misc/dataTransfer/Out.py")
        self.transferOut.value = 10000

        self.s3type = Attribute()
        self.s3type.inject("https://github.com/supermuesli/csdl", "aws/s3/S3Type.py")
        self.s3type.value = "standard"

        self.getAmount = Attribute()
        self.getAmount.inject("https://github.com/supermuesli/csdl", "misc/requests/GETAmount.py")
        self.getAmount.value = 13000

        self.postAmount = Attribute()
        self.postAmount.inject("https://github.com/supermuesli/csdl", "misc/requests/POSTAmount.py")
        self.postAmount.value = 10420

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
        self.s3type.value = "standardInfreqAccess"

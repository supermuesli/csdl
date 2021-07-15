from csdl import *


class EC2A1Large(VMAsAService):
    def __init__(self):
        # inherited fields
        self.name = "Elastic Cloud Compute a1.large"
        self.provider = "Amazon Web Services"
        self.tags = ["aws", "ec2", "virtual machine", "vm"]
        self.readme = "enjoy"
        self.gitRepo = "https://github.com/supermuesli/csdl"
        self.filePath = "aws/ec2/a1large.py"

        self.cpuCores.value = 4
        self.cpuCores.mutable = False

        self.ram.value = 4
        self.ram.mutable = False

        self.region = ChoiceAttribute()
        self.region.inject("https://github.com/supermuesli/csdl", "aws/region.py")
        self.region.value = "East Virgina"
        self.region.mutable = True

        self.storage = StorageAsAService()
        self.storage.inject("https://github.com/supermuesli/csdl", "aws/ebs.py")
        self.storage.mutable = True

        # non-inherited fields
        self.elasticIps = NumericAttribute()
        self.elasticIps.makeInt = True
        self.elasticIps.mutable = True

        # price
        self.price = Price()
        self.price.currency.inject("https://github.com/supermuesli/csdl", "currency.py")
        self.price.currency.value = "dollar"
        self.price.currency.mutable = False
        self.price.priceFuncs = []

        self.price.model = Hybrid()
        self.price.model.upFrontCost = 0
        self.price.model.billingPeriod = 1 # per hour



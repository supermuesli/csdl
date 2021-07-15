from csdl import *


class A1Large(VMAsAService):
    def __init__(self):
        super().__init__()
        # inherited fields
        self.name = "Elastic Cloud Compute a1.large"
        self.provider = "Amazon Web Services"
        self.tags = ["aws", "ec2", "virtual machine", "vm"]
        self.readme = "enjoy"
        self.gitRepo = "https://github.com/supermuesli/csdl"
        self.filePath = "aws/ec2/A1Large.py"

        self.cpuCores.value = 4
        self.cpuCores.mutable = False

        self.ram.value = 4
        self.ram.mutable = False

        self.region = ChoiceAttribute()
        self.region.inject("https://github.com/supermuesli/csdl", "aws/Region.py")
        self.region.value = self.region.options[1]  # you need to know beforehand which index is legal by checking out the git repository
        self.region.mutable = False

        self.storage = StorageAsAService()
        self.storage.inject("https://github.com/supermuesli/csdl", "aws/EBS.py")
        self.storage.mutable = True

        # non-inherited fields
        self.elasticIpAmount = NumericAttribute()
        self.elasticIpAmount.makeInt = True
        self.elasticIpAmount.mutable = True

        # price functions
        class elasticIpPrice(PriceFunc):
            def __init__(self):
                super().__init__()

            def run(self, req: Attribute):
                # iterate over all fields of the given requirement and check for the elasticIpAmount ID
                fields = vars(req)  # https://stackoverflow.com/a/55320647
                for key in fields:
                    if fields[key].id is not None:
                        if fields[key].id == self.elasticIpAmount.id:
                            if req.elasticIpAmount.value == 1:
                                return 2
                            if req.elasticIpAmount.value > 1:
                                return req.elasticIpAmount.value * 2.5
                return 0

        # price
        self.price = Price()
        self.price.currency.inject("https://github.com/supermuesli/csdl", "misc/Currency.py")
        self.price.currency.value = self.price.currency.options[0]
        self.price.currency.mutable = False
        self.price.priceFuncs = [elasticIpPrice()]

        self.price.model = Hybrid()
        self.price.model.upFrontCost = 0
        self.price.model.billingPeriod = 1  # per hour

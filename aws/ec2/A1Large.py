from csdl import *


class A1Large(VMAsAService):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/ec2/A1Large.py")

        # inherited fields
        self.name = "Elastic Cloud Compute a1.large"
        self.provider = "Amazon Web Services"
        self.tags = ["aws", "ec2", "virtual machine", "vm"]
        self.readme = "enjoy"

        self.cpuCores.value = 4
        self.cpuCores.mutable = False

        self.ram.value = 4
        self.ram.mutable = False

        self.region = ChoiceAttribute()
        self.region.inject("https://github.com/supermuesli/csdl", "aws/Region.py")
        self.region.value = self.region.options[1]  # you need to know beforehand which index is legal by checking out the git repository. a pyCharm plugin might help with this
        self.region.mutable = False

        self.storage = StorageAsAService()
        self.storage.inject("https://github.com/supermuesli/csdl", "aws/EBS.py")
        self.storage.mutable = True

        # non-inherited fields
        self.elasticIpAmount = NumericAttribute()
        self.elasticIpAmount.inject("https://github.com/supermuesli/csdl", "aws/ec2/ElasticIpAmount.py")
        self.elasticIpAmount.mutable = True

        # price functions
        class elasticIpPrice(PriceFunc):
            def __init__(self):
                super().__init__()

            def run(self, req: Attribute):
                # iterate over all fields of the given requirement and check for the elasticIpAmount ID
                fields = vars(req)  # https://stackoverflow.com/a/55320647
                for key in fields:
                    try:
                        if fields[key].id == "https://github.com/supermuesli/csdl/aws/ec2/ElasticIpAmount.py":
                            if fields[key].value == 1:
                                return 2
                            if fields[key].value > 1:
                                return fields[key].value * 2.5
                    except:
                        pass
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

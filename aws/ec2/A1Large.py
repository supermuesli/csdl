from csdl import *


class A1Large(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/ec2/A1Large.py")
        self.extendsId = "VMAsAService"

        # inherited fields
        self.name = "Elastic Cloud Compute a1.large"
        self.provider = "Amazon Web Services"
        self.searchKeyWords = ["aws", "ec2", "virtual machine", "vm", "a1 large"]  # help users find this model
        self.readme = "enjoy"

        self.cpuCores.value = 4
        self.cpuCores.mutable = True

        self.ram.value = 4
        self.ram.maxVal = 128
        self.ram.mutable = False

        self.region.inject("https://github.com/supermuesli/csdl", "aws/regions/Region.py")
        self.region.mutable = True

        # deactivate/delete Attribute that you don't want to include in matching
        self.storage = None
        self.storageWriteSpeed = None
        self.storageReadSpeed = None

        self.ebs = StorageAsAService()
        self.ebs.inject("https://github.com/supermuesli/csdl", "aws/EBS.py")
        self.ebs.mutable = True

        # non-inherited fields
        self.elasticIpAmount = NumericAttribute()
        self.elasticIpAmount.inject("https://github.com/supermuesli/csdl", "aws/ec2/ElasticIpAmount.py")
        self.elasticIpAmount.mutable = True

        # price functions
        class elasticIpPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "the amount of elastic ips specified takes a toll on the price"

            def run(self, req):
                # check if the requirement contains an elasticIpAmount field inside a VMAsAService
                match = matchField(req, "https://github.com/supermuesli/csdl@aws/ec2/ElasticIpAmount.py@latest")

                # if there was a match, then we can compute the price
                if match is not None:
                    if match.value == 1:
                        return 2
                    if match.value > 1:
                        return match.value * 2.5

                # otherwise we assume a default value and the corresponding price (0 IPs cost 0 us-dollar)
                return 0

        class defaultPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "what you pay regardless of all configurations"

            def run(self, req):
                return 1.25

        # price
        self.price.currency.inject("https://github.com/supermuesli/csdl", "misc/currencies/FeritsCurrencies.py")
        self.price.currency.choice = self.price.currency.options[0]  # US-Dollar
        self.price.priceFuncs = [defaultPrice(), elasticIpPrice()] + self.ebs.price.priceFuncs

        self.price.model = Subscription()
        self.price.model.billingPeriod = 1  # per hour

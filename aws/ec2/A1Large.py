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
        self.cpuCores.mutable = False  # attributes are immutable by default. this is just for demonstration

        self.ram.value = 4

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
            def __init__(self, topClass):
                super().__init__()
                self.description = "the amount of elastic ips specified takes a toll on the price"
                self.topClass = topClass

            def run(self, req):
                # check if the requirement contains an elasticIpAmount field inside an A1Large instance
                match = matchField(req, "ServerAsAService", "https://github.com/supermuesli/csdl@aws/ec2/ElasticIpAmount.py@latest")

                # if there was a match, then we can compute the price
                if match is not None:
                    if match.value is not None:  # a match does not automatically mean that the value is set
                        if match.value == 1:
                            return 2
                        if match.value > 1:
                            return match.value * 2.5

                # otherwise we assume a default value and the corresponding price (0 IPs cost 0 EUR)
                return 0

        class defaultPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "what you pay regardless of all configurations"

            def run(self, req):
                return 1.25

        # price
        self.price.currency = "USD"  # ISO 4217
        self.price.priceFuncs = [defaultPrice(), elasticIpPrice(self)] + self.ebs.price.priceFuncs

        self.price.model.choice = "subscription"
        self.price.model.options[self.price.model.choice].billingPeriod = 1  # once per hour

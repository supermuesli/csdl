from csdl import *


class A1Large(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/ec2/A1Large.py")
        self.extendsId = "VMAsAService"

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
                self.description = "the amount of elastic ips specified takes a toll on the price"

            def run(self, req):
                # check if the requirement contains an elasticIpAmount field
                match = matchField(req, "https://github.com/supermuesli/csdl/aws/ec2/ElasticIpAmount.py@latest")

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
        self.price = Price()
        self.price.currency.inject("https://github.com/supermuesli/csdl", "misc/Currency.py")
        self.price.currency.value = self.price.currency.options[0]  # index needs to be known by the user. a pycharm plugin might help
        self.price.priceFuncs = [defaultPrice(), elasticIpPrice()] + self.storage.price.priceFuncs

        self.price.model = Subscription()
        self.price.model.billingPeriod = 1  # per hour

from csdl import *


class EC2(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/ec2/EC2.py")
        self.extendsId = "VMAsAService"

        # inherited fields
        self.name = "Elastic Cloud Compute"
        self.provider = "Amazon Web Services"
        self.searchKeyWords = ["aws", "ec2", "virtual machine", "vm", "a1 large"]  # help users find this model
        self.readme = "enjoy"

        self.region.inject("https://github.com/supermuesli/csdl", "aws/regions/Region.py")
        self.region.mutable = True

        self.machineType = ChoiceAttribute()
        self.machineType.inject("https://github.com/supermuesli/csdl", "aws/ec2/MachineType.py")

        # deactivate fields that get covered by self.machineType
        self.cpuCores = None
        self.ram = None
        self.storage = None

        self.elasticIpAmount = NumericAttribute()
        self.elasticIpAmount.inject("https://github.com/supermuesli/csdl", "aws/ec2/ElasticIpAmount.py")
        self.elasticIpAmount.mutable = True

        # price functions
        class elasticIpPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "the amount of elastic ips specified takes a toll on the price"

            def run(self, req):
                # check if the requirement contains an elasticIpAmount field inside an EC2 instance
                match = matchAttribute(req, "https://github.com/supermuesli/csdl@aws/ec2/EC2.py@latest", "https://github.com/supermuesli/csdl@aws/ec2/ElasticIpAmount.py@latest")

                # if there was a match, then we can compute the price
                if match is not None:
                    if match.model is not None:  # a match does not automatically mean that the value is set
                        if match.model == 1:
                            return 2
                        if match.model > 1:
                            return match.model * 2.5

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
        self.price.priceFuncs = [defaultPrice(), elasticIpPrice()]

        self.price.model.model = "subscription"
        self.price.model.options[self.price.model.model].billingPeriod = 1  # once per hour

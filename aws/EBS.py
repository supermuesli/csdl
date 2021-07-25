from csdl import *


class EBS(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/EBS.py")
        self.extendsId = "StorageAsAService"

        self.name = "Elastic Block Storage"
        self.readme = "my email is: blabla@exmaple.com . i will answer any questions that you have :)"
        self.provider = "Amazon Web Services"
        self.searchKeyWords = ["aws", "ec2", "virtual machine", "vm"]

        self.storageReadSpeed.value = 1000
        self.storageReadSpeed.mutable = False

        self.storageWriteSpeed.value = 500
        self.storageWriteSpeed.mutable = False

        self.storage.makeInt = True
        self.storage.minVal = 5
        self.storage.maxVal = 10000
        self.storage.mutable = True

        self.region.inject("https://github.com/supermuesli/csdl", "aws/regions/Region.py")
        self.region.mutable = True

        class defaultPrice(PriceFunc):
            def __init__(self, topClass):
                super().__init__()
                self.description = "what you pay regardless of all configurations"
                self.topClass = topClass

            def run(self, req):
                # get attribute with the id Storage
                match = matchField(req, "Storage")
                if match is not None:
                    return 1.25*match.value

                return self.topClass.storage.minVal * 1.25

        # price
        self.price.currency.choice = "EUR"  # EUR
        self.price.priceFuncs = [defaultPrice(self)]

        self.price.model.choice = "subscription"  # subscription
        self.price.model.billingPeriod = 1  # per hour

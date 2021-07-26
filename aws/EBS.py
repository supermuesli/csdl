from csdl import *


class EBS(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/EBS.py")
        self.extendsId = "StorageAsAService"

        self.name = "Elastic Block Storage"
        self.readme = "my email is: blabla@exmaple.com . i will answer any questions that you have :)"
        self.provider = "Amazon Web Services"
        self.searchKeyWords = ["aws", "elastic block storage", "ebs"]

        self.storageReadSpeed.value = 1000

        self.storageWriteSpeed.value = 500

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
                match = matchField(req, self.topClass.id, "Storage")
                if match is not None:  # there was a match
                    if match.value is not None:  # a match does not automatically mean that the value is set
                        return 1.25*match.value

                return self.topClass.storage.minVal * 1.25

        # price
        self.price.currency = "EUR"  # EUR
        self.price.priceFuncs = [defaultPrice(self)]

        self.price.model.choice = "subscription"  # subscription
        self.price.model.options[self.price.model.choice].billingPeriod = 1  # once per hour

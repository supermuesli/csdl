from csdl import *


class EBS(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/EBS.py")
        self.extendsId = "StorageAsAService"

        self.name = "Elastic Block Storage"
        self.readme = "my email is: blabla@exmaple.com . i will answer any questions that you have :)"

        self.storageReadSpeed.value = 1000
        self.storageReadSpeed.mutable = False

        self.storageWriteSpeed.value = 500
        self.storageWriteSpeed.mutable = False

        self.storage.makeInt = True
        self.storage.minVal = 5
        self.storage.maxVal = 10000
        self.storage.mutable = True

        class defaultPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "what you pay regardless of all configurations"

            def run(self, req):
                # get attribute with the id StorageAsAService
                match = matchField(req, "StorageAsAService")
                if match is not None:
                    return 1.25*match.storage.value

                return self.storage.minVal * 1.25

        # price
        self.price = Price()
        self.price.currency.inject("https://github.com/supermuesli/csdl", "misc/Currency.py")
        self.price.currency.value = self.price.currency.options[0]
        self.price.currency.mutable = False
        self.price.priceFuncs = [defaultPrice()]

        self.price.model = Hybrid()
        self.price.model.upFrontCost = 50
        self.price.model.billingPeriod = 1  # per hour

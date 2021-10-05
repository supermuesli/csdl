from csdl import *


class S3(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/s3/S3.py")
        self.extendsId = "StorageAsAService"

        # inherited fields
        self.name = "Simple server storage"
        self.provider = "Amazon Web Services"
        self.searchKeyWords = ["aws", "s3", "storage as a service", "storage"]  # help users find this model
        self.readme = "enjoy"

        self.region.inject("https://github.com/supermuesli/csdl", "aws/regions/Region.py")
        self.region.mutable = True

        # price functions
        class defaultPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "what you pay regardless of all configurations"

            def run(self, req):
                return 1.25

        # price
        self.price.currency = "USD"  # ISO 4217
        self.price.priceFuncs = [defaultPrice()]

        self.price.model.value = "subscription"
        self.price.model.options[self.price.value.value].billingPeriod = 1  # once per hour

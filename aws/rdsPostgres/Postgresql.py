from csdl import *


class Postgresql(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/rdsPostgres/Postgresql.py")
        self.extendsId = "SQLDatabaseAsAService"

        # inherited fields
        self.name = "Managed PostgreSQL"
        self.provider = "Amazon Web Services"
        self.searchKeyWords = ["aws", "psql", "database as a service", "db", "postgres"]  # help users find this model
        self.readme = "enjoy"

        self.storage.mutable = True

        self.region.inject("https://github.com/supermuesli/csdl", "aws/regions/Region.py")
        self.region.mutable = True

        # storage type
        self.azDeployment = Attribute()
        self.azDeployment.inject("https://github.com/supermuesli/csdl", "aws/rdsPostgres/AvailabilityZone.py")
        self.azDeployment.mutable = True

        # price functions
        class defaultPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "what you pay regardless of all configurations"

            def run(self, req):
                return 0

        class storagePrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "raw storage price per billing period (1 month)"

            def run(self, req):
                # discover a storage field in req
                storageMatch = matchAttribute(req, "Storage")

                # discover an s3type field in req
                s3typeMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@aws/s3/S3Type.py@latest")

                # discover a region field in req
                regionMatch = matchAttribute(req, "Region")

                if regionMatch is not None:   # there was a match
                    if regionMatch.value is not None:  # matching value is set
                        if regionMatch.value == "northernVirginia":

                            if s3typeMatch is not None:  # there was a match
                                if s3typeMatch.value is not None:  # matching value is set
                                    if s3typeMatch.value == "standardInfreqAccess":

                                        if storageMatch is not None:  # there was a match
                                            if storageMatch.value is not None:  # matching value is set
                                                return storageMatch.value * 0.0125

                                    if s3typeMatch.value == "standard":

                                        if storageMatch is not None:  # there was a match
                                            if storageMatch.value is not None:  # matching value is set
                                                if storageMatch.value <= 50 * 1000:               # first 50 TB/Month
                                                    return storageMatch.value * 0.023
                                                if 50 * 1000 < storageMatch.value <= 450 * 1000:  # next 450 TB/Month
                                                    return storageMatch.value * 0.022
                                                if 500 * 1000 < storageMatch.value:               # over 500 TB/Month
                                                    return storageMatch.value * 0.021

                return 0

        # price
        self.price.currency = "USD"  # ISO 4217
        self.price.priceFuncs = [defaultPrice(), storagePrice()]  # https://calculator.aws/#/createCalculator/S3

        self.price.model.value = "subscription"
        self.price.model.options[self.price.model.value].billingPeriod = 24*28  # in hours

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

        self.storage.mutable = True

        self.region.inject("https://github.com/supermuesli/csdl", "aws/regions/Region.py")
        self.region.mutable = True

        # storage type
        self.s3Type = Attribute()
        self.s3Type.inject("https://github.com/supermuesli/csdl", "aws/s3/S3Type.py")
        self.s3Type.value = "standard"  # default to standard
        self.s3Type.mutable = True

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
                        if regionMatch.value == "northernVirgina":

                            if s3typeMatch is not None:  # there was a match
                                if s3typeMatch.value is not None:  # matching value is set
                                    if s3typeMatch.value == "standardInfreqAccess":

                                        if storageMatch is not None:  # there was a match
                                            if storageMatch.value is not None:  # matching value is set
                                                return storageMatch.value * 0.0125

                # else default to s3-standard in northern virginia
                if storageMatch is not None:  # there was a match
                    if storageMatch.value is not None:  # matching value is set
                        if storageMatch.value <= 50 * 1000:               # first 50 TB/Month
                            return storageMatch.value * 0.023
                        if 50 * 1000 < storageMatch.value <= 450 * 1000:  # next 450 TB/Month
                            return storageMatch.value * 0.022
                        if 500 * 1000 < storageMatch.value:               # over 500 TB/Month
                            return storageMatch.value * 0.021

                return 0

        class requestsPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "what you pay per 1000 PUT, COPY, POST, GET, SELECT and LIST reqeusts per billing period (1 month)"

            def run(self, req):
                res = 0

                # discover an S3Type field in req
                s3typeMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@aws/s3/S3Type.py@latest")

                # discover a region field in req
                regionMatch = matchAttribute(req, "Region")

                # discover a PUTAmount field in req
                putAmountMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/requests/PUTAmount.py@latest")

                # discover a COPYAmount field in req
                copyAmountMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/requests/COPYAmount.py@latest")

                # discover a LISTAmount field in req
                listAmountMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/requests/LISTAmount.py@latest")

                # discover a POSTAmount field in req
                postAmountMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/requests/POSTAmount.py@latest")

                # discover a GETAmount field in req
                getAmountMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/requests/GETAmount.py@latest")

                # discover a SELECTAmount field in req
                selectAmountMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/requests/SELECTAmount.py@latest")

                if regionMatch is not None:
                    if regionMatch.value is not None:
                        if regionMatch.value == "northernVirginia":
                            if putAmountMatch is not None:
                                if putAmountMatch.value is not None:
                                    if s3typeMatch is not None:
                                        if s3typeMatch.value is not None:
                                            if s3typeMatch.value == "standardInfreqAccess":
                                                res += 0.01 * putAmountMatch.value / 1000  # PUTAmount per billing period (1 month)
                                            elif s3typeMatch.value == "standard":
                                                res += 0.005 * putAmountMatch.value / 1000

                            if copyAmountMatch is not None:
                                if copyAmountMatch.value is not None:
                                    if s3typeMatch is not None:
                                        if s3typeMatch.value is not None:
                                            if s3typeMatch.value == "standardInfreqAccess":
                                                res += 0.01 * copyAmountMatch.value / 1000  # COPYAmount per billing period (1 month)
                                            elif s3typeMatch.value == "standard":
                                                res += 0.005 * copyAmountMatch.value / 1000

                            if postAmountMatch is not None:
                                if postAmountMatch.value is not None:
                                    if s3typeMatch is not None:
                                        if s3typeMatch.value is not None:
                                            if s3typeMatch.value == "standardInfreqAccess":
                                                res += 0.01 * postAmountMatch.value / 1000  # POSTAmount per billing period (1 month)
                                            elif s3typeMatch.value == "standard":
                                                res += 0.005 * postAmountMatch.value / 1000

                            if listAmountMatch is not None:
                                if listAmountMatch.value is not None:
                                    if s3typeMatch is not None:
                                        if s3typeMatch.value is not None:
                                            if s3typeMatch.value == "standardInfreqAccess":
                                                res += 0.01 * listAmountMatch.value / 1000  # LISTAmount per billing period (1 month)
                                            elif s3typeMatch.value == "standard":
                                                res += 0.005 * listAmountMatch.value / 1000

                            if getAmountMatch is not None:
                                if getAmountMatch.value is not None:
                                    if s3typeMatch is not None:
                                        if s3typeMatch.value is not None:
                                            if s3typeMatch.value == "standardInfreqAccess":
                                                res += 0.001 * getAmountMatch.value / 1000  # GETAmount per billing period (1 month)
                                            elif s3typeMatch.value == "standard":
                                                res += 0.0004 * getAmountMatch.value / 1000

                            if selectAmountMatch is not None:
                                if selectAmountMatch.value is not None:
                                    if s3typeMatch is not None:
                                        if s3typeMatch.value is not None:
                                            if s3typeMatch.value == "standardInfreqAccess":
                                                res += 0.001 * selectAmountMatch.value / 1000  # SELECTAmount per billing period (1 month)
                                            elif s3typeMatch.value == "standard":
                                                res += 0.0004 * selectAmountMatch.value / 1000

                return res

        class dataTransferPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "what you pay for data transfer in and out of the storage server per billing period (1 month)"

            def run(self, req):
                res = 0

                # discover a region field in req
                regionMatch = matchAttribute(req, "Region")

                # discover a region field in req
                transferInMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/dataTransfer/In.py@latest")

                # discover a region field in req
                transferOutMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/dataTransfer/Out.py@latest")

                if regionMatch is not None:
                    if regionMatch.value is not None:
                        if regionMatch.value == "northernVirginia":

                            if transferInMatch is not None:
                                if transferInMatch.value is not None:
                                    res += 0.00 * transferInMatch.value  # upload is free

                            if transferOutMatch is not None:
                                if transferOutMatch.value is not None:
                                    if transferOutMatch.value <= 1:
                                        res += 0.00 * transferOutMatch.value
                                    elif 1 < transferOutMatch.value <= 9.99*1000:
                                        res += 0.09 * transferOutMatch.value
                                    elif 9.99*1000 < transferOutMatch.value <= 40*1000:
                                        res += 0.085 * transferOutMatch.value
                                    elif 40*1000 < transferOutMatch.value <= 150*1000:
                                        res += 0.07 * transferOutMatch.value
                                    elif 150*1000 < transferOutMatch.value:
                                        res += 0.05 * transferOutMatch.value

                return res

        # price
        self.price.currency = "USD"  # ISO 4217
        self.price.priceFuncs = [defaultPrice(), storagePrice(), requestsPrice(), dataTransferPrice()]

        self.price.model.value = "subscription"
        self.price.model.options[self.price.model.value].billingPeriod = 24*28  # in hours

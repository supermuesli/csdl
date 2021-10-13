from csdl import *


class Postgresql(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "azure/postgres/Postgresql.py")
        self.extendsId = "SQLDatabaseAsAService"

        # inherited fields
        self.name = "Managed PostgreSQL"
        self.provider = "Microsoft Azure"
        self.searchKeyWords = ["azure", "psql", "database as a service", "db", "postgres"]  # help users find this model
        self.readme = "enjoy"

        self.storage = Storage()
        self.storage.mutable = True

        eastUs = Attribute()
        eastUs.inject("https://github.com/supermuesli/csdl", "misc/countries/EastUS.py")
        self.region = Region()
        self.region.options = {
            "eastUs": eastUs
        }
        self.region.mutable = True

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

        class dbInstancePrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "price per database instance per hour"

            def run(self, req):
                # discover an availabilityZone field in req
                azMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@aws/rdsPostgres/AvailabilityZone.py@latest")

                # discover a region field in req
                regionMatch = matchAttribute(req, "Region")

                ramMatch = matchAttribute(req, "Ram")
                cpuMatch = matchAttribute(req, "CpuCores")

                if ramMatch is not None:
                    if ramMatch.value is not None:
                        if cpuMatch is not None:
                            if cpuMatch.value is not None:
                                # figure out which ec2 instance matches with given ram and cpu
                                # https://aws.amazon.com/ec2/instance-types/t4/

                                if ramMatch.value == 1 and cpuMatch.value == 1:
                                    # dbt4gmicro

                                    if azMatch is not None:
                                        if azMatch.value is not None:
                                            if azMatch.value == "single":

                                                if regionMatch is not None:
                                                    if regionMatch.value is not None:
                                                        if regionMatch.value == "northernVirginia":
                                                            return 0.016

                                            if azMatch.value == "multi":

                                                if regionMatch is not None:
                                                    if regionMatch.value is not None:
                                                        if regionMatch.value == "northernVirginia":
                                                            return 0.032

                # defaults to t4gmicro with single availability zone in northernVirginia
                return 0.016

        class storagePrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "price per database instance per hour"

            def run(self, req):
                # discover an ssd storage field in req
                ssdStorageMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/storage/SSDStorage.py@latest")

                # discover an ssd storage field in req
                iopsSsdStorageMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/storage/IOPSSSDStorage.py@latest")

                # discover an ssd storage field in req
                iopsMagneticStorageMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/storage/IOPSMagneticStorage.py@latest")

                # default to general purpose ssd storage
                if ssdStorageMatch is None and iopsMagneticStorageMatch is None and iopsSsdStorageMatch is None:
                    ssdStorageMatch = matchAttribute(req, "Storage")

                    if ssdStorageMatch is None:
                        return 0

                # discover an availabilityZone field in req
                azMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@aws/rdsPostgres/AvailabilityZone.py@latest")

                # discover a region field in req
                regionMatch = matchAttribute(req, "Region")

                if azMatch is not None:
                    if azMatch.value is not None:
                        if azMatch.value == "single":

                            if regionMatch is not None:
                                if regionMatch.value is not None:
                                    if regionMatch.value == "northernVirginia":

                                        if ssdStorageMatch is not None:
                                            if ssdStorageMatch.value is not None:
                                                # general purpose ssd stoarge single availability zone
                                                return 0.115 * ssdStorageMatch.value / (24*28)

                                        if iopsSsdStorageMatch is not None:
                                            if iopsSsdStorageMatch.value is not None:

                                                # provisioned iops ssd storage single availability zone
                                                storageRes = 0.125 * iopsSsdStorageMatch.value
                                                iopsRes = 0.10 * iopsSsdStorageMatch.iops.value
                                                return (storageRes + iopsRes) / (24*28) # price description on the website was
                                                                           # per month, so we converted that to
                                                                           # per hour, since that is the billing
                                                                           # period

                                        if iopsMagneticStorageMatch is not None:
                                            if iopsMagneticStorageMatch.value is not None:
                                                # magnetic storage single availability zone
                                                storageRes = 0.10 * iopsMagneticStorageMatch.value
                                                iopsRes = 0.10 * iopsMagneticStorageMatch.iops.value / 1000000
                                                return (storageRes + iopsRes) / (24*28) # price description on the website was
                                                                           # per month, so we converted that to
                                                                           # per hour, since that is the billing
                                                                           # period
                                    else:
                                        # region matches, just not with northernVirginia. fallback to a reasonable default
                                        if ssdStorageMatch is not None:
                                            if ssdStorageMatch.value is not None:
                                                # general purpose ssd stoarge single availability zone
                                                return 0.115 * ssdStorageMatch.value / (24*28)

                                        if iopsSsdStorageMatch is not None:
                                            if iopsSsdStorageMatch.value is not None:

                                                # provisioned iops ssd storage single availability zone
                                                storageRes = 0.125 * iopsSsdStorageMatch.value
                                                iopsRes = 0.10 * iopsSsdStorageMatch.iops.value
                                                return (storageRes + iopsRes) / (24*28) # price description on the website was
                                                                           # per month, so we converted that to
                                                                           # per hour, since that is the billing
                                                                           # period

                                        if iopsMagneticStorageMatch is not None:
                                            if iopsMagneticStorageMatch.value is not None:
                                                # magnetic storage single availability zone
                                                storageRes = 0.10 * iopsMagneticStorageMatch.value
                                                iopsRes = 0.10 * iopsMagneticStorageMatch.iops.value / 1000000
                                                return (storageRes + iopsRes) / (24*28) # price description on the website was
                                                                           # per month, so we converted that to
                                                                           # per hour, since that is the billing
                                                                           # period

                        if azMatch.value == "multi":

                            if regionMatch is not None:
                                if regionMatch.value is not None:
                                    if regionMatch.value == "northernVirginia":

                                        if ssdStorageMatch is not None:
                                            if ssdStorageMatch.value is not None:
                                                # general purpose ssd stoarge multi availability zone
                                                return 0.23 * ssdStorageMatch.value / (24*28)

                                        if iopsSsdStorageMatch is not None:
                                            if iopsSsdStorageMatch.value is not None:
                                                # provisioned iops ssd storage multi availability zone
                                                storageRes = 0.25 * iopsSsdStorageMatch.value
                                                iopsRes = 0.20 * iopsSsdStorageMatch.iops.value
                                                return (storageRes + iopsRes) / (24*28) # price description on the website was
                                                                           # per month, so we converted that to
                                                                           # per hour, since that is the billing
                                                                           # period

                                        if iopsMagneticStorageMatch is not None:
                                            if iopsMagneticStorageMatch.value is not None:
                                                # magnetic storage multi availability zone
                                                storageRes = 0.20 * iopsMagneticStorageMatch.value
                                                iopsRes = 0.10 * iopsMagneticStorageMatch.iops.value / 1000000
                                                return (storageRes + iopsRes) / (24*28) # price description on the website was
                                                                           # per month, so we converted that to
                                                                           # per hour, since that is the billing
                                                                           # period

                return 0

        class backupPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "price per database instance per hour"

            def run(self, req):
                # how long to keep a backup per billing period (1 hour)
                retentionPeriodMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/storage/BackupRetentionPeriod.py@latest")

                # how many backup snapshots to make per billing period (1 hour)
                snapshotAmountMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/storage/BackupSnapshotAmount.py@latest")

                # how much storage is provisioned per billing period (1 hour)
                storageMatch = matchAttribute(req, "Storage")

                if storageMatch is not None:
                    if storageMatch.value is not None:

                        if snapshotAmountMatch is not None:
                            if snapshotAmountMatch.value is not None:

                                # 100% worth of storage backup is free per month
                                if snapshotAmountMatch.value > 0:

                                    if retentionPeriodMatch is not None:
                                        if retentionPeriodMatch.value is not None:
                                            if retentionPeriodMatch.value > 0:
                                                # since the billing period is per hour, the user probably wants to keep the backups for at least a month, but is forced
                                                # to provide a retentionperiod relative to the billing period. we scale the provided value down to a per month value here, as
                                                # an estimate.
                                                return 0.095 * storageMatch.value * snapshotAmountMatch.value * retentionPeriodMatch.value / (24*28)

                return 0

        class dataTransferPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "what you pay for data transfer in and out of the storage server per billing period (1 hour)"

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
                                    if 1 < transferOutMatch.value <= 1 + 9.999 * 1000:
                                        res += 0.09 * transferOutMatch.value
                                    elif 1 + 9.999 * 1000 < transferOutMatch.value <= 1 + (9.999 + 40) * 1000:
                                        res += 0.085 * transferOutMatch.value
                                    elif 1 + (9.999 + 40) * 1000 < transferOutMatch.value <= 1 + (
                                            9.999 + 40 + 100) * 1000:
                                        res += 0.07 * transferOutMatch.value
                                    elif 1 + (9.999 + 40 + 100) * 1000 < transferOutMatch.value:
                                        res += 0.05 * transferOutMatch.value

                return res

        # price
        self.price.currency = "USD"  # ISO 4217
        self.price.priceFuncs = [defaultPrice(), dbInstancePrice(), storagePrice(), backupPrice(), dataTransferPrice()]  # https://calculator.aws/#/createCalculator/RDSPostgreSQL

        self.price.model.value = "subscription"
        self.price.model.options[self.price.model.value].upfrontCost = 0
        self.price.model.options[self.price.model.value].billingPeriod = 1  # in hours

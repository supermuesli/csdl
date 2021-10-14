from csdl import *


class Postgresql(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "azure/postgres/Postgresql.py")
        self.extendsId = "SQLDatabaseAsAService"

        # inherited fields
        self.name = "Microsoft Azure - Managed PostgreSQL"
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

        self.workloadType = Attribute()
        self.workloadType.inject("https://github.com/supermuesli/csdl", "azure/postgres/WorkloadType.py")
        self.workloadType.value = "singleServer"  # default to singleServer

        self.machineType = Attribute()
        self.machineType.inject("https://github.com/supermuesli/csdl", "azure/postgres/MachineType.py")
        self.machineType.value = "generalPurpose1"  # default to basic1

        class dbInstancePrice(PriceFunc):
            def __init__(self, defaultWorkloadType, defaultMachineType):
                super().__init__()
                self.description = "price per database instance per hour"
                self.defaultWorkloadType = defaultWorkloadType
                self.defaultMachineType = defaultMachineType

            def run(self, req):
                workloadMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@azure/postgres/Workload.py@latest")
                if workloadMatch is None:
                    workloadMatch = self.defaultWorkloadType

                machineTypeMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@azure/postgres/MachineType.py@latest")

                regionMatch = matchAttribute(req, "Region")
                ramMatch = matchAttribute(req, "Ram")
                cpuMatch = matchAttribute(req, "CpuCores")

                if machineTypeMatch is None and ramMatch is None and cpuMatch is None:
                    machineTypeMatch = self.defaultMachineType

                if workloadMatch is not None:
                    if workloadMatch.value is not None:
                        if workloadMatch.value == "singleServer":

                            if machineTypeMatch is not None:
                                if machineTypeMatch.value is not None:
                                    if machineTypeMatch.value == "basic1":
                                        return 0.034

                                    if machineTypeMatch.value == "generalPurpose1":
                                        return 0.176

                            if ramMatch is not None:
                                if ramMatch.value is not None:
                                    if cpuMatch is not None:
                                        if cpuMatch.value is not None:
                                            if (ramMatch.value <= 2) and (cpuMatch.value <= 1):
                                                if regionMatch is not None:
                                                    if regionMatch.value is not None:
                                                        if regionMatch.value == "eastUs":
                                                            return 0.034
                                            elif (ramMatch.value <= 4) and (cpuMatch.value <= 2):
                                                if regionMatch is not None:
                                                    if regionMatch.value is not None:
                                                        if regionMatch.value == "eastUs":
                                                            return 0.068
                                            elif (ramMatch.value <= 10) and (cpuMatch.value <= 2):
                                                if regionMatch is not None:
                                                    if regionMatch.value is not None:
                                                        if regionMatch.value == "eastUs":
                                                            return 0.176

                # defaults to generalPurpose1 with single server in eastUs
                return 0.176

        class storagePrice(PriceFunc):
            def __init__(self, defaultWorkloadType, defaultMachineType):
                super().__init__()
                self.description = "storage price per hour"
                self.defaultWorkloadType = defaultWorkloadType
                self.defaultMachineType = defaultMachineType

            def run(self, req):
                res = 0

                storageMatch = matchAttribute(req, "Storage")

                workloadMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@azure/postgres/Workload.py@latest")
                if workloadMatch is None:
                    workloadMatch = self.defaultWorkloadType

                machineTypeMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@azure/postgres/MachineType.py@latest")

                regionMatch = matchAttribute(req, "Region")
                ramMatch = matchAttribute(req, "Ram")
                cpuMatch = matchAttribute(req, "CpuCores")

                if machineTypeMatch is None and ramMatch is None and cpuMatch is None:
                    machineTypeMatch = self.defaultMachineType

                if workloadMatch is not None:
                    if workloadMatch.value is not None:
                        if workloadMatch.value == "singleServer":

                            if machineTypeMatch is not None:
                                if machineTypeMatch.value is not None:
                                    if machineTypeMatch.value == "basic1":
                                        if storageMatch is not None:
                                            if storageMatch.value is not None:
                                                res += 0.10 * storageMatch.value / (24*28)

                                    if machineTypeMatch.value == "generalPurpose1":
                                        if storageMatch is not None:
                                            if storageMatch.value is not None:
                                                res += 0.115 * storageMatch.value / (24*28)

                            if ramMatch is not None:
                                if ramMatch.value is not None:
                                    if cpuMatch is not None:
                                        if cpuMatch.value is not None:
                                            if (ramMatch.value <= 2) and (cpuMatch.value <= 1):
                                                if regionMatch is not None:
                                                    if regionMatch.value is not None:
                                                        if regionMatch.value == "eastUs":
                                                            if storageMatch is not None:
                                                                if storageMatch.value is not None:
                                                                    res += 0.10 * storageMatch.value / (24*28)
                                            elif (ramMatch.value <= 4) and (cpuMatch.value <= 2):
                                                if regionMatch is not None:
                                                    if regionMatch.value is not None:
                                                        if regionMatch.value == "eastUs":
                                                            if storageMatch is not None:
                                                                if storageMatch.value is not None:
                                                                    res += 0.10 * storageMatch.value / (24*28)

                                            elif (ramMatch.value <= 10) and (cpuMatch.value <= 2):
                                                if regionMatch is not None:
                                                    if regionMatch.value is not None:
                                                        if regionMatch.value == "eastUs":
                                                            if storageMatch is not None:
                                                                if storageMatch.value is not None:
                                                                    res += 0.115 * storageMatch.value / (24*28)

                return res

        class backupPrice(PriceFunc):
            def __init__(self):
                super().__init__()
                self.description = "backup price per hour"

            def run(self, req):
                retentionPeriodMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/storage/BackupRetentionPeriod.py@latest")
                snapshotAmountMatch = matchAttribute(req, "https://github.com/supermuesli/csdl@misc/storage/BackupSnapshotAmount.py@latest")
                storageMatch = matchAttribute(req, "Storage")

                if storageMatch is not None:
                    if storageMatch.value is not None:

                        if snapshotAmountMatch is not None:
                            if snapshotAmountMatch.value is not None:
                                if snapshotAmountMatch.value > 0:

                                    if retentionPeriodMatch is not None:
                                        if retentionPeriodMatch.value is not None:
                                            if retentionPeriodMatch.value > 0:
                                                return (0.10 / (24*28)) * (storageMatch.value *24*28) * (snapshotAmountMatch.value / (24*28)) * (retentionPeriodMatch.value / (24*28))

                return 0

        # price
        self.price.currency = "USD"  # ISO 4217
        self.price.priceFuncs = [dbInstancePrice(self.workloadType, self.machineType), storagePrice(self.workloadType, self.machineType), backupPrice()]

        self.price.model.value = "subscription"
        self.price.model.options[self.price.model.value].upfrontCost = 0
        self.price.model.options[self.price.model.value].billingPeriod = 1  # in hours

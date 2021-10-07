from csdl import *


class DatabaseRequirement(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/DatabaseRequirement.py")
        self.extendsId = "DatabaseAsAService"

        usa = OptionAttribute()
        usa.inject("https://github.com/supermuesli/csdl", "misc/countries/USA.py")
        self.region = Region()
        self.region.options.update({
            "usa": usa
        })
        self.region.value = "usa"

        self.storage = Storage()
        self.storage.value = 900

        self.backupRetention = Attribute()
        self.backupRetention.inject("https://github.com/supermuesli/csdl", "misc/storage/BackupRetentionPeriod.py")
        self.backupRetention.value = 1  # keep for 3 billing period

        self.backupSnapshots = Attribute()
        self.backupSnapshots.inject("https://github.com/supermuesli/csdl", "misc/storage/BackupSnapshotAmount.py")
        self.backupSnapshots.value = 1  # 1 per billing period

        self.transferIn = Attribute()
        self.transferIn.inject("https://github.com/supermuesli/csdl", "misc/dataTransfer/In.py")
        self.transferIn.value = 10005

        self.transferOut = Attribute()
        self.transferOut.inject("https://github.com/supermuesli/csdl", "misc/dataTransfer/Out.py")
        self.transferOut.value = 1000
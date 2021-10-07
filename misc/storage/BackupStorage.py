from csdl import *


class BackupStorage(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "misc/storage/BackupStorage.py")
        self.extendsId = "Storage"

        self.retentionPeriod = Attribute()
        self.retentionPeriod.inject("https://github.com/supermuesli/csdl@misc/storage/BackupRetentionPeriod.py@latest")

        self.snapshots = Attribute()
        self.snapshots.inject("https://github.com/supermuesli/csdl@misc/storage/BackupSnapshotAmount.py@latest")

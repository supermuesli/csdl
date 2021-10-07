from csdl import *


# basically ec2 instances


class StorageType(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/rdsPostgres/StorageType.py")
        self.extendsId = "ChoiceAttribute"

        dbt4gmicro = OptionAttribute()
        dbt4gmicro.inject("https://github.com/supermuesli/csdl", "aws/rdsPostgres/DbT4gMicro.py")

        self.options = {
            "dbt4gmicro": dbt4gmicro
        }
        self.value = None

        self.mutable = True

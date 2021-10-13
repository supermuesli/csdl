from csdl import *


class WorkloadType(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "azure/postgres/WorkloadType.py")
        self.extendsId = "ChoiceAttribute"

        singleServer = OptionAttribute()
        singleServer.inject("https://github.com/supermuesli/csdl", "azure/postgres/SingleServer.py")

        self.options = {
            "singleServer": singleServer
        }
        self.value = None

        self.mutable = True

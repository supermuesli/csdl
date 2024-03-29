from csdl import *


class MachineType(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "azure/postgres/MachineType.py")
        self.extendsId = "ChoiceAttribute"

        basic1 = OptionAttribute()
        basic1.inject("https://github.com/supermuesli/csdl", "azure/postgres/Basic1.py")

        generalPurpose1 = OptionAttribute()
        generalPurpose1.inject("https://github.com/supermuesli/csdl", "azure/postgres/GeneralPurpose1.py")

        self.options = {
            "basic1": basic1,
            "generalPurpose1": generalPurpose1
        }
        self.value = None

        self.mutable = True

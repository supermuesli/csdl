from csdl import *


class AvailabilityZone(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/auroraDB/AvailabilityZone.py")
        self.extendsId = "ChoiceAttribute"

        single = OptionAttribute()
        single.inject("https://github.com/supermuesli/csdl", "aws/auroraDB/SingleAZ.py")

        multi = OptionAttribute()
        multi.inject("https://github.com/supermuesli/csdl", "aws/auroraDB/MultiAZ.py")

        self.options = {
            "single": single,
            "multi": multi
        }
        self.value = None

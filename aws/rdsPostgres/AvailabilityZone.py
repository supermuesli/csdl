from csdl import *


class AvailabilityZone(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/rdsPostgres/AvailabilityZone.py")
        self.extendsId = "ChoiceAttribute"

        single = OptionAttribute()
        single.inject("https://github.com/supermuesli/csdl", "aws/rdsPostgres/SingleAZ.py")

        multi = OptionAttribute()
        multi.inject("https://github.com/supermuesli/csdl", "aws/rdsPostgres/MultiAZ.py")

        self.options = {
            "single": single,
            "multi": multi
        }
        self.value = None

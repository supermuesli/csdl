from csdl import *


class DatabaseRequirement(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/DatabaseRequirement.py")
        self.extendsId = "DatabaseAsAService"

        self.ram.value = 4
        self.cpuCores.value = 4
        self.storage.value = 500

        self.staticIpAddresses = NumericAttribute()
        self.staticIpAddresses.inject("https://github.com/supermuesli/csdl", "misc/StaticIp.py")
        self.staticIpAddresses.value = 2

        usa = OptionAttribute()
        usa.inject("https://github.com/supermuesli/csdl", "misc/countries/USA.py")
        self.region.value = "usa"

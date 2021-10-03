from csdl import *


class Requirement1(Attribute):  # does not have to extend VMAsAService since injection will already refactor the code to do it later, but
                                # it is good practise to be explicit and do it anyway. also, the IDE should make better autocompletions that way
                                # . note that custom attributes cannot be extended, so the closest related Attribute
                                # should be extended instead.
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/Requirement1.py")
        self.extendsId = "VMAsAService"

        self.ram.model = 4
        self.cpuCores.model = 4
        self.storage.model = 500

        self.staticIpAddresses = NumericAttribute()
        self.staticIpAddresses.inject("https://github.com/supermuesli/csdl", "misc/StaticIp.py")
        self.staticIpAddresses.value = 2

        usa = OptionAttribute()
        usa.inject("https://github.com/supermuesli/csdl", "misc/countries/USA.py")
        self.region.options = {
            "usa": usa
        }
        self.region.model = "usa"

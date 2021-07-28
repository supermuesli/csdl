from csdl import *


class Requirement1(Attribute):  # does not have to extend VMAsAService sind injection will already refactor the code to do it later, but
                                # it is good practise to be explicit and do it anyway. also, the IDE should make better autocompletions that way
                                # . note that custom attributes cannot be extended, however, so the closest related Attribute
                                # should be extended instead.
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/Requirement1.py")
        self.extendsId = "VMAsAService"

        self.ram.value = 4
        self.cpuCores.value = 4
        self.storage.value = 500

        self.staticIpAddresses = NumericAttribute()
        self.staticIpAddresses.inject("https://github.com/supermuesli/csdl", "misc/StaticIp.py")
        self.staticIpAddresses.value = 200

        usa = OptionAttribute()
        usa.inject("https://github.com/supermuesli/csdl", "misc/countries/USA.py")
        self.region.options = {
            "usa": usa
        }
        self.region.choice = "usa"
        
        self.price.model.choice = "subscription"  # pay per resource

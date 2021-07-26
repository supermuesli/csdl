from csdl import *


class Requirement1(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/Requirement1.py")
        self.extendsId = "VMAsAService"

        self.ram.value = 4
        self.cpuCores.value = 4
        self.storage.value = 50

        self.staticIpAddresses = NumericAttribute()
        self.staticIpAddresses.inject("https://github.com/supermuesli/csdl", "misc/StaticIp.py")
        self.staticIpAddresses.value = 200

        self.region.choice = "northAmerica"
        self.price.model.choice = "subscription"  # pay per resource
        self.price.currency = "EUR"

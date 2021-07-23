from csdl import *


class Requirement1(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/Requirement1.py")
        self.extendsId = "VMAsAService"

        self.ram.value = 16
        self.cpuCores.value = 129
        self.storage.storage.value = 500

        self.staticIpAddresses = NumericAttribute()
        self.staticIpAddresses.inject("https://github.com/supermuesli/csdl", "misc/StaticIp.py")
        self.staticIpAddresses.value = 5

        self.region.choice = self.region.options[0]  # Europe

        self.price.currency.choice = self.price.currency.options[0]  # USD
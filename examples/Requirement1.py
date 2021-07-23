from csdl import *


class Requirement1(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/Requirement1.py")
        self.extendsId = "VMAsAService"

        self.ram.value = 16
        self.cpuCores.value = 129
        self.storage.storage.value = 50

        self.staticIpAddresses = NumericAttribute()
        self.staticIpAddresses.inject("https://github.com/supermuesli/csdl", "misc/StaticIp.py")
        self.staticIpAddresses.value = 15

        self.price.currency.choice = self.price.currency.options[0]  # USD
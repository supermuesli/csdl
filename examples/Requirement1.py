from csdl import *


class Requirement1(CCS):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "examples/Requirement1.py")
        self.extendsId = "VMAsAService"

        self.ram.value = 16
        self.cpuCores.value = 4
        self.storage.storage.value = 50

        self.staticIpAddresses = NumericAttribute()
        self.staticIpAddresses.inject("https://github.com/supermuesli/csdl", "misc/StaticIp.py")
        self.staticIpAddresses.value = 2
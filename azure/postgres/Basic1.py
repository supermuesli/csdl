from csdl import *


class Basic1(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "azure/postgres/Basic1.py")
        self.extendsId = "OptionAttribute"

        self.cpuCores = CpuCores()
        self.cpuCores.value = 1
        self.cpuCores.mutable = False  # attributes are immutable by default. this is just for demonstration

        self.ram = Ram()
        self.ram.value = 2
        self.ram.mutable = False  # attributes are immutable by default. this is just for demonstration

from csdl import *


class A1Large(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/ec2/A1Large.py")
        self.extendsId = "OptionAttribute"

        self.cpuCores = CpuCores()
        self.cpuCores.value = 4
        self.cpuCores.mutable = False  # attributes are immutable by default. this is just for demonstration

        self.ram = Ram()
        self.ram.value = 4
        self.ram.mutable = False  # attributes are immutable by default. this is just for demonstration

        self.ebs = StorageAsAService()
        self.ebs.inject("https://github.com/supermuesli/csdl", "aws/EBS.py")
        self.ebs.mutable = True

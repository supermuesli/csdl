from csdl import *

# https://aws.amazon.com/ec2/instance-types/t4/


class DbT4gMicro(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/rdsPostgres/DbT4gMicro.py")
        self.extendsId = "OptionAttribute"

        self.cpuCores = CpuCores()
        self.cpuCores.value = 2
        self.cpuCores.mutable = False  # attributes are immutable by default. this is just for demonstration

        self.ram = Ram()
        self.ram.value = 1
        self.ram.mutable = False  # attributes are immutable by default. this is just for demonstration

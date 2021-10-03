from csdl import *


class MachineType(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/ec2/MachineType.py")
        self.extendsId = "ChoiceAttribute"

        a1large = Attribute()
        a1large.inject("https://github.com/supermuesli/csdl", "aws/ec2/A1Large.py")

        self.options = {
            "a1large": a1large
        }
        self.value = None

        self.mutable = True

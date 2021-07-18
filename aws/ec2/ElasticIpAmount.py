from csdl import *


class ElasticIpAmount(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/ec2/ElasticIpAmount.py")
        self.extendsId = "https://github.com/supermuesli/csdl@misc/StaticIp.py@latest"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.stepSize = 1

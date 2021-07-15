from csdl import *


class ElasticIpAmount(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.gitRepo = "https://github.com/supermuesli/csdl"
        self.filePath = "aws/ec2/ElasticIpAmount.py"
        self.setId()

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.stepSize = 1

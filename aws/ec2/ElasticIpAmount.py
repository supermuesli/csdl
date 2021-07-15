from csdl import *


class ElasticIpAmount(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.makeInt = True
        self.minVal = 0
        self.stepSize = 1

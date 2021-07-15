from csdl import *


class EBS(StorageAsAService):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/EBS.py", original=True)

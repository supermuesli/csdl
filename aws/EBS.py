from csdl import *


class EBS(StorageAsAService):
    def __init__(self):
        self.gitRepo = "https://github.com/supermuesli/csdl"
        self.filePath = "aws/EBS.py"
        self.setId()
        super().__init__()

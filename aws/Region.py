from csdl import *


class Region(ChoiceAttribute):
    def __init__(self):
        super().__init__()
        self.gitRepo = "https://github.com/supermuesli/csdl"
        self.filePath = "aws/Region.py"
        self.setId()

        self.options = ["East Virginia", "New York", "California"]

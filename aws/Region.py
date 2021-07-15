from csdl import *


class Region(ChoiceAttribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/Region.py")

        self.options = ["East Virginia", "New York", "California"]

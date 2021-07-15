from csdl import *


class Region(ChoiceAttribute):
    def __init__(self):
        super().__init__()
        self.options = ["East Virginia", "New York", "California"]

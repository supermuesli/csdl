from csdl import *


class Currency(ChoiceAttribute):
    def __init__(self):
        super().__init__()
        self.options = ["us-dollar", "euro", "yen"]

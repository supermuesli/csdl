from csdl import *


class NewYork(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/regions/NewYork.py")
        self.extendsId = "https://github.com/supermuesli/csdl@misc/countries/USA.py@latest"

        self.value = "New York"

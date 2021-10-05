from csdl import *


class NorthernVirginia(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/regions/NorthernVirginia.py")
        self.extendsId = "https://github.com/supermuesli/csdl@misc/countries/USA.py@latest"

        self.name = "N. Virgina"

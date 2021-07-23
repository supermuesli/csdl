from csdl import *


class EastVirgina(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/regions/EastVirgina.py")
        self.extendsId = "https://github.com/supermuesli/csdl@misc/countries/USA.py@latest"

        self.value = "East Virgina"

from csdl import *


class California(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/regions/California.py")
        self.extendsId = "https://github.com/supermuesli/csdl@misc/countries/USA.py@latest"

        self.value = "California"

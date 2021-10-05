from csdl import *


class S3Type(Attribute):
    def __init__(self):
        super().__init__()
        self.setId("https://github.com/supermuesli/csdl", "aws/s3/S3Type.py")
        self.extendsId = "ChoiceAttribute"

        standard = OptionAttribute()
        standard.inject("https://github.com/supermuesli/csdl", "aws/s3/Standard.py")

        standardInfreqAccess = OptionAttribute()
        standardInfreqAccess.inject("https://github.com/supermuesli/csdl", "aws/s3/StandardInfreqAccess.py")

        self.options = {
            "standard": standard,
            "standardInfreqAccess": standardInfreqAccess
        }
        self.value = None

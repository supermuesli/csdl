from csdl import Attribute
from math import inf


class Region(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "Region"
        self.extendsId = "ChoiceAttribute"
        self.description = "The continent in which the CCS resides"

        self.options = ["Europe", "North America", "South America", "East Asia", "Antarctica", "Africa", "Australia"]
        self.value = self.options[0]


class Currency(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "Currency"
        self.extendsId = "ChoiceAttribute"
        self.description = "The currency in which the price is charged"

        self.options = ["US-Dollar", "Euro", "Yen"]
        self.value = self.options[0]


class Storage(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "Storage"
        self.extendsId = "NumericAttribute"
        self.description = "Storage amount in GB"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class StorageWriteSpeed(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "StorageWriteSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "Storage write speed in GB/s"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class StorageReadSpeed(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "StorageWriteSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "Storage read speed in GB/s"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class OperatingSystem(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "OperatingSystem"
        self.extendsId = "ChoiceAttribute"
        self.description = "The operating system a CCS runs on"

        self.options = ["Linux", "Windows", "Mac"]
        self.value = self.options[0]


class CpuCores(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "CpuCores"
        self.extendsId = "NumericAttribute"
        self.description = "The amount of CPU cores"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class CpuClockSpeed(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "CpuClockSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "CPU clock speed in GHz"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class Ram(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "Ram"
        self.extendsId = "NumericAttribute"
        self.description = "The amount of Ram in GB"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class RamClockSpeed(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "RamClockSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "RAM clock speed in GHz"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class RamWriteSpeed(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "RamWriteSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "RAM write speed in GB/s"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class RamReadSpeed(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "RamReadSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "RAM read speed in GB/s"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class NetworkCapacity(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "NetworkCapacity"
        self.extendsId = "NumericAttribute"
        self.description = "Network capacity in GB"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class NetworkUploadSpeed(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "NetworkUploadSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "Network upload speed in GB/s"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class NetworkDownloadSpeed(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "NetworkDownloadSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "Network download speed in GB/s"

        self.value = 0
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True

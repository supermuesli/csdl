import sys
import tempfile
import importlib.util
from abc import ABC, abstractmethod
from dulwich import porcelain


class Attribute:
    def __init__(self):
        super().__init__()
        self.name = None
        self.gitRepo = None
        self.filePath = None
        self.mutable = False

    def inject(self, gitRepo, filePath):
        self.gitRepo = gitRepo
        self.filePath = filePath

        # git clone metamodel repository
        tempDir = tempfile.TemporaryDirectory()
        porcelain.clone(self.gitRepo, tempDir.name)

        modulePath = tempDir.name + "/" + filePath
        moduleName = filePath.split("/")[-1].split(".py")[0]
        moduleDir = ''.join(modulePath.split(moduleName + ".py"))
        print("modulePath: ", modulePath)
        print("moduleName: ", moduleName)
        print("moduleDir: ", moduleDir)

        # spec = importlib.util.spec_from_file_location(tempDir.name, modulePath)
        # module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(module)
        # sys.modules[tempDir.name] = module
        # print("module: ", module)

        sys.path.insert(1, moduleDir)
        exec("from " + moduleName + " import *")
        exec("global " + moduleName)
        exec("self = " + moduleName + "()")

        tempDir.cleanup()


class BoolAttribute(Attribute):
    def __init__(self):
        super().__init__()
        self.value = None


class ChoiceAttribute(Attribute):
    def __init__(self):
        super().__init__()
        self.value = None
        self.options = None


class NumericAttribute(Attribute):
    def __init__(self):
        super().__init__()
        self.value = None
        self.minVal = None
        self.maxVal = None
        self.stepSize = None
        self.makeInt = False


class PricingModel:
    def __init__(self):
        super().__init__()
        self.description = None


class Subscription(PricingModel):
    def __init__(self):
        super().__init__()
        self.billingPeriod = None


class PayAndGo(PricingModel):
    def __init__(self):
        super().__init__()
        self.upFrontCost = None


class Hybrid(PricingModel):
    def __init__(self):
        super().__init__()
        self.upFrontCost = None
        self.billingPeriod = None


class PayPerResource(Subscription):
    def __init__(self):
        pass


class Price(ABC):
    def __init__(self):
        super().__init__()
        self.currency = ChoiceAttribute()
        self.priceFuncs = []
        self.model = None

    @abstractmethod
    def get(self, req: Attribute):
        return sum(pf.run(req) for pf in self.priceFuncs)


# an interface as per https://stackoverflow.com/questions/2124190/how-do-i-implement-interfaces-in-python
class PriceFunc(ABC):
    def __init__(self):
        super().__init__()
        self.description = None
        self.value = 0

    @abstractmethod
    def run(self, req: Attribute):
        pass


class CCS(Attribute):
    def __init__(self):
        super().__init__()
        self.price = None


class IaaS(CCS):
    def __init__(self):
        super().__init__()
        self.region = ChoiceAttribute()


class StorageAsAService(IaaS):
    def __init__(self):
        super().__init__()
        self.storage = NumericAttribute()
        self.storageWriteSpeed = NumericAttribute()
        self.storageReadSpeed = NumericAttribute()


class ServerAsAService(IaaS):
    def __init__(self):
        super().__init__()
        self.os = ChoiceAttribute()
        self.cpuCores = NumericAttribute()
        self.cpuClockSpeed = NumericAttribute()
        self.ram = NumericAttribute()
        self.ramClockSpeed = NumericAttribute()
        self.ramWriteSpeed = NumericAttribute()
        self.ramReadSpeed = NumericAttribute()
        self.networkCapacity = NumericAttribute()
        self.networkUploadSpeed = NumericAttribute()
        self.networkDownloadSpeed = NumericAttribute()


class VMAsAService(ServerAsAService):
    def __init__(self):
        super().__init__()
        self.storage = StorageAsAService()


class SaaS(CCS):
    def __init__(self):
        super().__init__()
        pass


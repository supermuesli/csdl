import sys
import tempfile
from abc import ABC, abstractmethod
from dulwich import porcelain


class Attribute:
    def __init__(self):
        super().__init__()
        self.name = None
        self.gitRepo = None
        self.commit = None
        self.filePath = None
        self.original = False
        self.id = None
        self.mutable = False

    def setId(self, gitRepo, filePath, original=True, commit=None):
        """ you call this if you create a new custom attribute """
        self.gitRepo = gitRepo
        self.commit = commit
        self.filePath = filePath
        self.original = original
        self.id = gitRepo + "/" + filePath
        if self.commit is not None and not self.original:
            self.id += "@" + self.commit
            self.commit = b"refs/heads/master/" + self.commit
        else:
            self.id += "@latest"

    def inject(self, gitRepo, filePath, commit=None):
        """ you call this if you want to use a custom attribute """
        self.setId(gitRepo, filePath, commit=commit, original=False)

        # git clone metamodel repository
        tempDir = tempfile.TemporaryDirectory()
        porcelain.clone(self.gitRepo, tempDir.name)
        if self.commit is not None:
            print("checkout commit " + self.commit)
            porcelain.update_head(tempDir.name, self.commit)

        # inject metamodel into this Attribute
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
        exec("self.__dict__.update(" + moduleName + "().__dict__)")  # this requires a class with the same name as the
        # moduleName. also read
        # https://stackoverflow.com/questions/1216356/is-it-safe-to-replace-a-self-object-by-another-object-of-the-same-type-in-a-meth/37658673#37658673

        #exec("global " + moduleName)                                 # read here https://stackoverflow.com/questions/11990556/how-to-make-global-imports-from-a-function

        if commit is not None:
            assert self.id == gitRepo + "/" + filePath + "@" + commit, "failed to inject CCS model properly. got %s but wanted %s" % (self.id, gitRepo + "/" + filePath + "@" + commit)
        else:
            assert self.id == gitRepo + "/" + filePath + "@latest", "failed to inject CCS model properly. got %s but wanted %s" % (self.id, gitRepo + "/" + filePath + "@latest")
        tempDir.cleanup()


class BoolAttribute(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "BoolAttribute"
        self.value = None


class ChoiceAttribute(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "ChoiceAttribute"
        self.value = None
        self.options = None


class NumericAttribute(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "NumericAttribute"
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


class Price:
    def __init__(self):
        super().__init__()
        self.currency = ChoiceAttribute()
        self.priceFuncs = []
        self.model = None

    def get(self, req):
        """ returns the total price """
        return sum(pf.run(req) for pf in self.priceFuncs)


# an interface as per https://stackoverflow.com/questions/2124190/how-do-i-implement-interfaces-in-python
class PriceFunc(ABC):
    def __init__(self):
        super().__init__()
        self.description = None
        self.value = 0

    @abstractmethod
    def run(self, req):
        """ returns the value of this price function """
        pass


class CCS(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "CCS"
        self.price = None


class IaaS(CCS):
    def __init__(self):
        super().__init__()
        self.id = "IaaS"
        self.region = ChoiceAttribute()


class StorageAsAService(IaaS):
    def __init__(self):
        super().__init__()
        self.id = "StorageAsAService"
        self.storage = NumericAttribute()
        self.storageWriteSpeed = NumericAttribute()
        self.storageReadSpeed = NumericAttribute()


class ServerAsAService(IaaS):
    def __init__(self):
        super().__init__()
        self.id = "ServerAsAService"
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
        self.id = "VMAsAService"
        self.storage = StorageAsAService()


class SaaS(CCS):
    def __init__(self):
        super().__init__()
        self.id = "SaaS"


def matchField(attribute, attributeId):
    """ get the field belonging to attribute with the given attributeId """
    fields = vars(attribute)  # https://stackoverflow.com/a/55320647
    for key in fields:
        try:
            if fields[key].id == attributeId:
                return fields[key]
        except:
            pass
    return None


def matchCCS(req, ccs):
    """ check if the requirements match with the given CCS """
    if type(req) is type(ccs):
        if type(ccs) is SaaS:
            # TODO addiontally match using the tags and fulltext or something. return True for now
            return True
        return True
    return False

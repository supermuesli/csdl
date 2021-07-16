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
        self.moreIsBetter = True


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
        self.region.id = "region"


class StorageAsAService(IaaS):
    def __init__(self):
        super().__init__()
        self.id = "StorageAsAService"
        self.storage = NumericAttribute()
        self.storage.id = "storage"
        self.storageWriteSpeed = NumericAttribute()
        self.storageWriteSpeed.id = "storageWriteSpeed"
        self.storageReadSpeed = NumericAttribute()
        self.storageReadSpeed.id = "storageReadSpeed"


class ServerAsAService(IaaS):
    def __init__(self):
        super().__init__()
        self.id = "ServerAsAService"
        self.os = ChoiceAttribute()
        self.os.id = "os"
        self.cpuCores = NumericAttribute()
        self.cpuCores.id = "cpuCores"
        self.cpuClockSpeed = NumericAttribute()
        self.cpuClockSpeed.id = "cpuClockSpeed"
        self.ram = NumericAttribute()
        self.ram.id = "ram"
        self.ramClockSpeed = NumericAttribute()
        self.ramClockSpeed.id = "ramClockSpeed"
        self.ramWriteSpeed = NumericAttribute()
        self.ramWriteSpeed.id = "ramWriteSpeed"
        self.ramReadSpeed = NumericAttribute()
        self.ramReadSpeed.id = "ramReadSpeed"
        self.networkCapacity = NumericAttribute()
        self.networkCapacity.id = "networkCapacity"
        self.networkUploadSpeed = NumericAttribute()
        self.networkUploadSpeed.id = "networkUploadSpeed"
        self.networkDownloadSpeed = NumericAttribute()
        self.networkDownloadSpeed.id = "networkDownloadSpeed"

class VMAsAService(ServerAsAService):
    def __init__(self):
        super().__init__()
        self.id = "VMAsAService"
        self.storage = StorageAsAService()


class SaaS(CCS):
    def __init__(self):
        super().__init__()
        self.id = "SaaS"


def extractAttributes(attribute):
    """ get all fields that are CSDL attributes """
    res = []
    fields = vars(attribute)  # https://stackoverflow.com/a/55320647
    for key in fields:
        try:
            if Attribute in fields[key].__class__.mro(): # https://stackoverflow.com/questions/31028237/getting-all-superclasses-in-python-3
                res += [fields[key]]
        except:
            pass
    return res


def matchField(attribute, attributeId):
    """ get the field belonging to attribute with the given attributeId.
        for all attributes all attribute fields must be unique """
    fields = vars(attribute)  # https://stackoverflow.com/a/55320647
    for key in fields:
        try:
            if fields[key].id == attributeId:
                return fields[key]
        except:
            pass
    return None


def matchCCS(req, ccs):
    """ check if requirements match with a given CCS """
    reqAttributes = extractAttributes(req)
    ccsAttributes = extractAttributes(ccs)

    for ra in reqAttributes:
        for ca in ccsAttributes:
            if ra.id == ca.id:
                if type(ra) is NumericAttribute:
                    if ra.value is not None and ca.value is None:  # requirement sets this attribute, but CCS does not
                        print(1)
                        return False
                    if ra.value is not None and ca.value is not None:  # both requirement and CCS set this attribute
                        if ca.moreIsBetter:
                            if not ca.mutable:
                                if ra.value < ca.value:  # value is too small and not mutable
                                    print(2)
                                    return False
                            if ca.maxVal is not None:
                                if ca.maxVal < ra.value:  # value cannot be made large enough
                                    print(3)
                                    return False
                        else:
                            if not ca.mutable:
                                if ra.value > ca.value:  # value is too large and not mutable
                                    print(4)
                                    return False
                            if ca.minVal is not None:
                                if ca.minVal > ra.value:  # value cannot be made small enough
                                    print(5)
                                    return False
                    reqAttributes.remove(ra)  # requirement is fulfilled
                elif type(ra) is BoolAttribute:
                    if not ca.mutable:
                        if ra.value != ca.value:  # value does not match and is not mutable
                            print(6)
                            return False
                    reqAttributes.remove(ra)  # requirement is fulfilled
                elif type(ra) is ChoiceAttribute:
                    if ca.mutable:
                        if ra.value not in ca.options:  # value mutable but not available
                            print(7)
                            return False
                    else:
                        if ra.value != ca.value:  # value does not match and is not mutable
                            print(8)
                            return False
                    reqAttributes.remove(ra)  # requirement is fulfilled

            if CCS in ra.__class__.mro():  # CCS is a super class of ra
                return matchCCS(req, ra)
    return True

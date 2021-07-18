import ast
import logging
import tempfile
from abc import ABC, abstractmethod
from commons import *
from dulwich import porcelain

""" caches all cloned git repositories """
ccsGitCache = {}

""" attributes that have already been injected """
injectedIds = {"VMAsAService", "ServerAsAService", "SaaS", "IaaS", "StorageAsAService", "NumericAttribute",
               "ChoiceAttribute", "BoolAttribute", "CCS", "Attribute"}


def cleanGitCache():
    """ delete all temporary directories that were created to clone git repositories into """
    gitRepos = []
    for gitRepo in ccsGitCache:
        ccsGitCache[gitRepo].cleanup()
        gitRepos += [gitRepo]
    for gitRepo in gitRepos:
        del ccsGitCache[gitRepo]


class Attribute:
    def __init__(self):
        super().__init__()
        self.name = None
        self.gitRepo = None
        self.commit = None
        self.filePath = None
        self.id = None
        self.extendsId = None
        self.mutable = False

    def setId(self, gitRepo, filePath, commit=None):
        """ you call this if you create a new custom attribute """
        self.gitRepo = gitRepo
        self.commit = commit
        self.filePath = filePath
        self.id = gitRepo + "@" + filePath
        if self.commit is not None:
            self.id += "@" + self.commit
            self.commit = "refs/heads/master/" + self.commit
        else:
            self.id += "@latest"

    def inject(self, gitRepo, filePath, commit=None):
        """ you call this if you want to use a custom attribute """
        self.setId(gitRepo, filePath, commit=commit)

        # git clone metamodel repository
        if gitRepo not in ccsGitCache:
            tempDir = tempfile.TemporaryDirectory()
            porcelain.clone(self.gitRepo, tempDir.name)
            ccsGitCache[gitRepo] = tempDir

        if self.commit is not None:
            print("checkout commit " + self.commit)
            porcelain.update_head(ccsGitCache[gitRepo].name, self.commit)
        # TODO else checkout latest commit ...

        # inject metamodel into this Attribute
        modulePath = ccsGitCache[gitRepo].name + "/" + filePath
        moduleName = filePath.split("/")[-1].split(".py")[0]
        moduleDir = ''.join(modulePath.split(moduleName + ".py"))
        # print("modulePath: ", modulePath)
        # print("moduleName: ", moduleName)
        # print("moduleDir: ", moduleDir)

        # parse module for extendsId field
        source = open(modulePath, "r").read()
        root = ast.parse(source)

        closestClass = None
        try:
            classes = [node for node in ast.walk(root) if isinstance(node, ast.ClassDef) and node.name == moduleName]
            closestClass = classes[0]
        except Exception as e:
            print(e)
            logging.error("can not inject %s because it does not define a class with the same name as its filename" % modulePath)

        closestFunction = None
        try:
            functions = [node for node in ast.walk(closestClass) if isinstance(node, ast.FunctionDef) and node.name == "__init__"]
            closestFunction = functions[0]
        except Exception as e:
            print(e)
            logging.error("can not inject %s because it does not define a __init__ function in its main class" % modulePath)

        closestAssign = None
        try:
            assigns = [node for node in ast.walk(closestFunction) if isinstance(node, ast.Assign)]
            assigns = [node for node in assigns if isinstance(node.targets[0], ast.Attribute)]
            assigns = [node for node in assigns if node.targets[0].attr == "extendsId"]
            closestAssign = assigns[0]
        except Exception as e:
            print(e)
            logging.error("can not inject %s because it does set the field extendsId" % modulePath)

        extendsId = closestAssign.value.value

        if extendsId not in injectedIds:
            dummy = CCS()
            dummyGitRepo = extendsId.split("@")[0]
            dummyFilePath = extendsId.split("@")[1]
            dummy.inject(dummyGitRepo, dummyFilePath)

        if extendsId not in ["VMAsAService", "ServerAsAService", "SaaS", "IaaS", "StorageAsAService", "NumericAttribute",
               "ChoiceAttribute", "BoolAttribute", "CCS", "Attribute"]:
            extendsId = extendsId.split("@")[1].split("/")[-1].split(".py")[0]  # extendsId as link/to/repo@file/path.py@commitSHA

        # print("extendsId: ", extendsId)

        # refactor source main class extension
        extensionDigitStart = source.find("class " + moduleName + "(") + len("class " + moduleName + "(")
        extensionDigitEnd = source.find(")", extensionDigitStart)
        source = source[:extensionDigitStart] + extendsId + source[extensionDigitEnd:]

        # import module directly from refactored source (inject)
        exec(source, globals())
        exec("self.__dict__.update(" + moduleName + "().__dict__)")  # this requires a class with the same name as the moduleName. also read
                                                                     # https://stackoverflow.com/questions/1216356/is-it-safe-to-replace-a-self-object-by-another-object-of-the-same-type-in-a-meth/37658673#37658673
        injectedIds.add(extendsId)
        print("injected", moduleName)

        # some asserts for early failure
        if commit is not None:
            assert self.id == gitRepo + "@" + filePath + "@" + commit, "failed to inject CCS model properly. got %s but wanted %s" % (self.id, gitRepo + "/" + filePath + "@" + commit)
        else:
            assert self.id == gitRepo + "@" + filePath + "@latest", "failed to inject CCS model properly. got %s but wanted %s" % (self.id, gitRepo + "/" + filePath + "@latest")


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


class Static(PricingModel):
    """ static pricing models only depend on the configuration of the CCS """
    def __init__(self):
        super().__init__()


class PayAndGo(Static):
    """ you (pay) an upFrontCost once (and go) on to use the service """
    def __init__(self):
        super().__init__()
        self.upFrontCost = None


class Subscription(Static):
    """ you pay a billingPeriodCost per billingPeriod. the unit of billingPeriod is per hour """
    def __init__(self):
        super().__init__()
        self.billingPeriodCost = None
        self.billingPeriod = None  # per hour


class PayPerResource(Static):
    """ you pay the price of each resource  per billingPeriod. the unit of billingPeriod is per hour """
    def __init__(self):
        super().__init__()


class Dynamic(PricingModel):
    """ dynamic pricing models depend on the configuration of the CCS and also on """
    def __init__(self):
        super().__init__()
        self.interpreter = None


class DataDriven(Dynamic):
    """ if python was not the metamodel language, then this datadriven dynamic pricing would not be possible. how else would
        you describe arbitrary callbacks using a selfmade DSL? it would be possible, but complicated to design a DSL that
        is in itself turing complete. it makes more sense to just use python directly
    """
    def __init__(self):
        super().__init__()
        self.dataset = None

    def getEstimatedPrice(self):
        """ estimate the price based on the given dataset. the interpreter has to be a function that interprets
            the dataset and returns the current price based on it. note that you have to implement the interpreter
            first. """
        return self.interpreter()


class Hybrid(PayAndGo, PayPerResource, Subscription, DataDriven):
    """ any combination of all pricing models. """
    def __init__(self):
        super().__init__()


class Price:
    """ everything to evaluate the final price based on CCS configuration and the pricing model enforced by the CCS """
    def __init__(self):
        super().__init__()
        self.currency = Currency()
        self.priceFuncs = []
        self.model = None

    def get(self, req, usageHours=0):
        """ returns the total price """
        if self.model.__class__ is PayAndGo:
            self.model.upFrontCost = sum([pf.run(req) for pf in self.priceFuncs])
            return self.model.upFrontCost

        if self.model.__class__ is Subscription:
            self.model.billingPeriodCost = sum([pf.run(req) for pf in self.priceFuncs])
            return usageHours/self.model.billingPeriod * self.model.billingPeriodCost

        if self.model.__class__ is PayPerResource:
            return sum([pf.run(req) for pf in self.priceFuncs])

        if self.model.__class__ is Hybrid:
            return self.model.interpreter()

        if self.model.__class__ is DataDriven:
            return self.model.getEstimatedPrice()

        # pricing model defaults to PayPerResource
        return sum([pf.run(req) for pf in self.priceFuncs])


# an interface as per https://stackoverflow.com/questions/2124190/how-do-i-implement-interfaces-in-python
class PriceFunc(ABC):
    def __init__(self):
        super().__init__()
        self.description = None

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

        self.region = Region()


class StorageAsAService(IaaS):
    def __init__(self):
        super().__init__()
        self.id = "StorageAsAService"

        self.storage = Storage()
        self.storageWriteSpeed = StorageWriteSpeed()
        self.storageReadSpeed = StorageReadSpeed()


class ServerAsAService(IaaS):
    def __init__(self):
        super().__init__()
        self.id = "ServerAsAService"

        self.os = OperatingSystem()
        self.cpuCores = CpuCores()
        self.cpuClockSpeed = CpuClockSpeed()
        self.ram = Ram()
        self.ramClockSpeed = RamClockSpeed()
        self.ramWriteSpeed = RamWriteSpeed()
        self.ramReadSpeed = RamReadSpeed()
        self.networkCapacity = NetworkCapacity()
        self.networkUploadSpeed = NetworkUploadSpeed()
        self.networkDownloadSpeed = NetworkDownloadSpeed()


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
    """ get all fields that are CCS attributes """
    res = []
    fields = vars(attribute)  # https://stackoverflow.com/a/55320647
    for key in fields:
        try:
            # this is also why CCS have to extend the Attribute class. matchCCS need CCS fields this to match requirements
            if Attribute in fields[key].__class__.mro(): # https://stackoverflow.com/questions/31028237/getting-all-superclasses-in-python-3
                res += [fields[key]]
        except:
            pass
    return res


def matchField(ccs, attributeId):
    """ get the field belonging to attribute with the given attributeId. if the given attribute already has the same
        attributeId, then the attribute will be returned. note that for all attributes all attribute fields must be
        unique
    """
    if ccs.id == attributeId:
        return ccs

    fields = vars(ccs)  # https://stackoverflow.com/a/55320647
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
                if ra.__class__ is NumericAttribute:
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
                    # requirement is fulfilled
                elif ra.__class__ is BoolAttribute:
                    if not ca.mutable:
                        if ra.value != ca.value:  # value does not match and is not mutable
                            print(6)
                            return False
                    # requirement is fulfilled
                elif ra.__class__ is ChoiceAttribute:
                    if ca.mutable:
                        if ra.value not in ca.options:  # value mutable but not available
                            print(7)
                            return False
                    else:
                        if ra.value != ca.value:  # value does not match and is not mutable
                            print(8)
                            return False
                    # requirement is fulfilled

                elif CCS in ca.__class__.mro():
                    return matchCCS(req, ca)
    return True

import ast
import logging
import tempfile
import random
import string
from abc import ABC, abstractmethod
from math import inf

from dulwich import porcelain

""" caches all cloned git repositories """
ccsGitCache = {}

""" attribute class names that have already been injected mapped to their attribute ids """
importedClasses = {
    "VMAsAService": "VMAsAService",
    "ServerAsAService": "ServerAsAService",
    "SaaS": "SaaS",
    "IaaS": "IaaS",
    "StorageAsAService": "StorageAsAService",
    "NumericAttribute": "NumericAttribute",
    "ChoiceAttribute": "ChoiceAttribute",
    "BoolAttribute": "BoolAttribute",
    "CCS": "CCS",
    "Attribute": "Attribute",
    "Region": "Region",
    "Currency": "Currency",
    "Storage": "Storage",
    "StorageWriteSpeed": "StorageWriteSpeed",
    "StorageReadSpeed": "StorageReadSpeed",
    "OperatingSystem": "OperatingSystem",
    "CpuCores": "CpuCores",
    "CpuClockSpeed": "CpuClockSpeed",
    "Ram": "Ram",
    "RamClockSpeed": "RamClockSpeed",
    "RamWriteSpeed": "RamWriteSpeed",
    "RamReadSpeed": "RamReadSpeed",
    "NetworkCapacity": "NetworkCapacity",
    "NetworkUploadSpeed": "NetworkUploadSpeed",
    "NetworkDownloadSpeed": "NetworkDownloadSpeed"
}


def cleanGitCache():
    """ delete all temporary directories that were created to clone git repositories into """
    gitRepos = []
    for gitRepo in ccsGitCache:
        ccsGitCache[gitRepo].cleanup()
        gitRepos += [gitRepo]
    for gitRepo in gitRepos:
        del ccsGitCache[gitRepo]


def randName():
    """ returns a cryptographically secure 16 digit random string starting with the letter C"""
    return "C" + "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))


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
        self.matched = False

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

    def inject(self, gitRepo, filePath, commit=None, onlyFetchDependency=False):
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
        moduleId = gitRepo + "@" + filePath + "@" + "latest"  # TODO make this work with given commit id too ...
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
        #print(modulePath, "extendsId: ", extendsId)

        # import extendsId module if it was not imported yet
        if extendsId not in importedClasses:
            print("fetch dependency first:", extendsId)
            dummy = CCS()
            try:
                dummyGitRepo = extendsId.split("@")[0]
                dummyFilePath = extendsId.split("@")[1]
            except Exception as e:
                print(e)
                logging.error("%s sets an extendsId field that is not formatted correctly. non-common attributes/CCS have \
to be of the form link/to/repo@file/path.py@(commitID|latest), however this was the given extendsId: '%s'" % (
                modulePath, extendsId))
                return
            dummy.inject(dummyGitRepo, dummyFilePath, onlyFetchDependency=True)

        # extract class name from extendsId
        # common attributes ids are already identical to their class names, so they don't need this step
        if extendsId not in ["CCS", "Attribute", "VMAsAService", "ServerAsAService", "SaaS", "IaaS", "StorageAsAService", "NumericAttribute",
                         "ChoiceAttribute", "BoolAttribute", "Region", "Currency", "Storage", "StorageWriteSpeed"
            , "StorageReadSpeed", "OperatingSystem", "CpuCores", "CpuClockSpeed", "Ram", "RamClockSpeed",
                         "RamWriteSpeed", "RamReadSpeed", "NetworkCapacity", "NetworkUploadSpeed", "NetworkDownloadSpeed"]:
            extendsId = importedClasses[extendsId]

        # NOTE that extendsId has been assigned its class name from here on out

        # refactor source main class name to a non-colliding class name
        # , as well as the extension class to the class name derived from its extendsId field
        if moduleId not in importedClasses:
            nonCollidingClassName = randName()  # this prevents accidental class overwriting when class names of injected
                                                # custom attributes happen to be identical
            try:
                extensionDigitStart = source.find("class " + moduleName + "(") + len("class ")  # NOTE this means that moduleName and the model main class name HAVE to be identical
                extensionDigitEnd = source.find(")", extensionDigitStart)
                source = source[:extensionDigitStart] + nonCollidingClassName + "(" + extendsId + source[extensionDigitEnd:]
            except Exception as e:
                print(e)
                logging.error("the injected module has to define a main class with the same name as its file name. the\
injected ccs/attribute models moduleName was %s, however no main class name that was identical to it was found in %s" % (moduleName, modulePath))
                return

            # debugging
            # print(source)
            
            # import module directly from refactored source
            exec(source, globals())
            importedClasses[moduleId] = nonCollidingClassName
            print("imported", moduleName, "with id", moduleId, "as", nonCollidingClassName)

        if not onlyFetchDependency:
            # inject custom class fields (overwrites/overrides existing fields and functions)
            exec("self.__dict__.update(" + importedClasses[moduleId] + "().__dict__)")  # read https://stackoverflow.com/questions/1216356/is-it-safe-to-replace-a-self-object-by-another-object-of-the-same-type-in-a-meth/37658673#37658673
            print("injected", moduleName, "into", self.extendsId)

        # some asserts for early failure
        if commit is not None:
            assert self.id == gitRepo + "@" + filePath + "@" + commit, "failed to inject CCS model properly. got %s but wanted %s" % (self.id, gitRepo + "@" + filePath + "@" + commit)
        else:
            assert self.id == gitRepo + "@" + filePath + "@latest", "failed to inject CCS model properly. got %s but wanted %s" % (self.id, gitRepo + "@" + filePath + "@latest")


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

        self.operatingSystem = OperatingSystem()
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
            # this is also why CCS should extend the Attribute class. matchCCS need CCS fields this to match requirements
            if Attribute in fields[key].__class__.mro(): # https://stackoverflow.com/questions/31028237/getting-all-superclasses-in-python-3
                res += [fields[key]]
        except Exception as e:
            logging.debug(e)
    return res


def matchField(ccs, attributeId):
    """ get the first field belonging to attribute with the given attributeId. if the given attribute already has the
        same attributeId, then the attribute will be returned. note that attribute values can be none if they are not
        initialised before matching.
    """
    if ccs.id == attributeId:
        return ccs

    fields = vars(ccs)  # https://stackoverflow.com/a/55320647
    for key in fields:
        try:
            if fields[key].id == attributeId:
                return fields[key]
        except Exception as e:
            logging.debug(e)
    return None


def matchCCS(req, ccs):
    """ recursively check if requirements match with a given CCS """
    reqAttributes = extractAttributes(req)
    ccsAttributes = extractAttributes(ccs)

    # pair-wise compare attributes and check if they match
    for ra in reqAttributes:
        if not ra.matched:
            for ca in ccsAttributes:
                if ra.id == ca.id:  # attributes match by id, now check if their values are satisfiable
                    # TODO if attributes don't match by id directly, check if subclasses match by id if they exist

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
                        # TODO mark requirement as matched

                    elif ra.__class__ is BoolAttribute:
                        if not ca.mutable:
                            if ra.value != ca.value:  # value does not match and is not mutable
                                print(6)
                                return False
                        # requirement is fulfilled
                        # TODO mark requirement as matched
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
                        # TODO mark requirement as matched

                    elif CCS in ca.__class__.mro():
                        return matchCCS(req, ca)
    return True


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

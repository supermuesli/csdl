import ast
import json
import logging
import math
import tempfile
import random
import string
from abc import ABC, abstractmethod
from math import inf

import graphviz
import requests
from dulwich import porcelain

ccsGitCache = {}
""" Caches all cloned git repositories """

importedClasses = {
    "VMAsAService": {
        "className": "VMAsAService",
        "extendsId": "ServerAsAService"
    },
    "ServerAsAService": {
        "className": "ServerAsAService",
        "extendsId": "IaaS"
    },
    "SaaS": {
        "className": "SaaS",
        "extendsId": "CCS"
    },
    "IaaS": {
        "className": "IaaS",
        "extendsId": "CCS"
    },
    "StorageAsAService": {
        "className": "StorageAsAService",
        "extendsId": "IaaS"
    },
    "NumericAttribute": {
        "className": "NumericAttribute",
        "extendsId": "Attribute"
    },
    "ChoiceAttribute": {
        "className": "ChoiceAttribute",
        "extendsId": "Attribute"
    },
    "BoolAttribute": {
        "className": "BoolAttribute",
        "extendsId": "Attribute"
    },
    "OptionAttribute": {
        "className": "OptionAttribute",
        "extendsId": "Attribute"
    },
    "CCS": {
        "className": "CCS",
        "extendsId": "Attribute"
    },
    "Attribute": {
        "className": "Attribute",
        "extendsId": "object"
    },
    "Region": {
        "className": "Region",
        "extendsId": "ChoiceAttribute"
    },
    "NorthAmerica": {
        "className": "NorthAmerica",
        "extendsId": "OptionAttribute"
    },
    "Australia": {
        "className": "Australia",
        "extendsId": "OptionAttribute"
    },
    "Africa": {
        "className": "Africa",
        "extendsId": "OptionAttribute"
    },
    "EastAsia": {
        "className": "EastAsia",
        "extendsId": "OptionAttribute"
    },
    "SouthAmerica": {
        "className": "SouthAmerica",
        "extendsId": "OptionAttribute"
    },
    "Europe": {
        "className": "Europe",
        "extendsId": "OptionAttribute"
    },
    "Antarctica": {
        "className": "Antarctica",
        "extendsId": "OptionAttribute"
    },
    "Storage": {
        "className": "Storage",
        "extendsId": "NumericAttribute"
    },
    "StorageWriteSpeed": {
        "className": "StorageWriteSpeed",
        "extendsId": "NumericAttribute"
    },
    "StorageReadSpeed": {
        "className": "StorageReadSpeed",
        "extendsId": "NumericAttribute"
    },
    "OperatingSystem": {
        "className": "OperatingSystem",
        "extendsId": "ChoiceAttribute"
    },
    "CpuCores": {
        "className": "CpuCores",
        "extendsId": "NumericAttribute"
    },
    "CpuClockSpeed": {
        "className": "CpuClockSpeed",
        "extendsId": "NumericAttribute"
    },
    "Ram": {
        "className": "Ram",
        "extendsId": "NumericAttribute"
    },
    "RamClockSpeed": {
        "className": "RamClockSpeed",
        "extendsId": "NumericAttribute"
    },
    "RamWriteSpeed": {
        "className": "RamWriteSpeed",
        "extendsId": "NumericAttribute"
    },
    "RamReadSpeed": {
        "className": "RamReadSpeed",
        "extendsId": "NumericAttribute"
    },
    "NetworkCapacity": {
        "className": "NetworkCapacity",
        "extendsId": "NumericAttribute"
    },
    "NetworkUploadSpeed": {
        "className": "NetworkUploadSpeed",
        "extendsId": "NumericAttribute"
    },
    "NetworkDownloadSpeed": {
        "className": "NetworkDownloadSpeed",
        "extendsId": "NumericAttribute"
    },
    "PricingModel": {
        "className": "PricingModel",
        "extendsId": "ChoiceAttribute"
    },
    "PayAndGo": {
        "className": "PayAndGo",
        "extendsId": "OptionAttribute"
    },
    "Subscription": {
        "className": "Subscription",
        "extendsId": "OptionAttribute"
    },
    "Price": {
        "className": "Price",
        "extendsId": "Attribute"
    },
    "DatabaseAsAService": {
        "className": "DatabaseAsAService",
        "extendsId": "SaaS"
    },
    "SQLDatabaseAsAService": {
        "className": "SQLDatabaseAsAService",
        "extendsId": "DatabaseAsAService"
    },
    "NoSQLDatabaseAsAService": {
        "className": "NoSQLDatabaseAsAService",
        "extendsId": "DatabaseAsAService"
    }
}
""" AttributeIds that have already been imported mapped to their class names and extendsIds. Whenever a new Attribute
    is added (not imported) to the framework, it needs to be included in here. """


def cleanGitCache():
    """ Delete all temporary directories that were created to clone git repositories into """
    gitRepos = []
    for gitRepo in ccsGitCache:
        ccsGitCache[gitRepo].cleanup()
        gitRepos += [gitRepo]
    for gitRepo in gitRepos:
        del ccsGitCache[gitRepo]


def randName():
    """ Returns a cryptographically secure 16 digit random string starting with the letter C"""
    return "C" + "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))


class Attribute:
    """ Instances of the Attribute class have a unique id that encodes from where they can be loaded. Classes that
        extend the Attribute class can be matched with other Attributes if they are related, which helps with user
        requirement matching and price calculation. Also, classes that have an Attribute type ancestor can be extended
        arbitrarily by other Attribute type instances (however, note that existing duplicate fields will be overwritten.
    """

    def __init__(self):
        super().__init__()
        self.name = None
        self.gitRepo = None
        self.commit = None
        self.branch = None
        self.filePath = None
        self.id = "Attribute"
        self.extendsId = "object"
        self.mutable = False
        self.searchKeyWords = None
        self.description = None
        self.matched = False
        self.value = None

    def setId(self, gitRepo, filePath, branch=None, commit=None):
        """ Set the id of an Attribute type instance. This id has to be unique and specify from where the Attribute can
            be loaded.

            Args:
                gitRepo (str): The URI to a git repository where the file is stored. Defaults to "local", indicating that it is stored on the local machine.
                filePath (str): The path to the file inside the git repository.
                branch (str): The git branch name, defaults to None (indicates that master should be fetched).
                commit (str): The commit id of the git branch, defaults to None (indicates that the latest commit should be fetched)
        """

        self.gitRepo = gitRepo
        self.commit = commit
        self.filePath = filePath
        self.id = gitRepo + "@" + filePath
        if self.commit is not None:
            self.id += "@" + self.commit
            self.commit = "refs/heads/master/" + self.commit
        else:
            self.id += "@latest"

    def inject(self, gitRepo, filePath, branch=None, commit=None, onlyFetchDependency=False):
        """ Updates self with the fields of the Attribute that are attained from the given filePath.

            Args:
                gitRepo (str): The URI to a git repository where the file is stored. Defaults to "local", indicating that it is stored on the local machine.
                filePath (str): The path to the file inside the git repository.
                branch (str): The git branch name, defaults to None (indicates that master should be fetched).
                commit (str): The commit id of the git branch, defaults to None (indicates that the latest commit should be fetched)
                onlyFetchDependency (bool): Does not inject any fields to self if set to True, defaults to False.
        """

        self.setId(gitRepo, filePath, branch=branch, commit=commit)

        # git clone metamodel repository
        if gitRepo not in ccsGitCache:
            tempDir = tempfile.TemporaryDirectory()
            porcelain.clone(self.gitRepo, tempDir.name)
            ccsGitCache[gitRepo] = tempDir

        if self.commit is not None:
            print("checkout commit " + self.commit)
            porcelain.update_head(ccsGitCache[gitRepo].name, self.commit)
        # TODO else checkout latest commit and branch...

        # inject metamodel into this Attribute
        moduleId = gitRepo + "@" + filePath + "@" + "latest"  # TODO make this work with given commit id and branch too
        modulePath = ccsGitCache[gitRepo].name + "/" + filePath
        moduleName = filePath.split("/")[-1].split(".py")[0]
        # moduleDir = ''.join(modulePath.split(moduleName + ".py"))
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
        # print(modulePath, "extendsId: ", extendsId)

        # import extendsId module if it was not imported yet
        if extendsId not in importedClasses:
            #print("fetch dependency first:", extendsId)
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
        extendsClassName = importedClasses[extendsId]["className"]

        # refactor source main class name to a non-colliding class name
        # , as well as the extension class to the class name derived from its extendsId field
        if moduleId not in importedClasses:
            nonCollidingClassName = randName()  # this prevents accidental class overwriting when class names of
            # injected custom attributes happen to be identical
            try:
                extensionDigitStart = source.find("class " + moduleName + "(") + len("class ")  # NOTE this means that moduleName and the model main class name HAVE to be identical
                extensionDigitEnd = source.find(")", extensionDigitStart)
                source = source[:extensionDigitStart] + nonCollidingClassName + "(" + extendsClassName + source[extensionDigitEnd:]
            except Exception as e:
                print(e)
                logging.error("the injected module has to define a main class with the same name as its file name. the \
injected ccs/attribute models moduleName was %s, however no main class name that was identical to it was found in %s" % (moduleName, modulePath))
                return

            # debugging
            # print(source)

            # import module directly from refactored source
            exec(source, globals())
            importedClasses[moduleId] = {}
            importedClasses[moduleId]["className"] = nonCollidingClassName
            importedClasses[moduleId]["extendsId"] = extendsId
            print("imported", moduleName, "with id", moduleId, "as", nonCollidingClassName)

        if not onlyFetchDependency:
            # inject custom class fields (overwrites/overrides existing fields and functions)
            exec("self.__dict__.update(" + importedClasses[moduleId]["className"] + "().__dict__)")  # read https://stackoverflow.com/questions/1216356/is-it-safe-to-replace-a-self-object-by-another-object-of-the-same-type-in-a-meth/37658673#37658673
            # print("injected", moduleName, "into", self.extendsId)

        # some asserts for early failure
        if commit is not None:
            assert self.id == gitRepo + "@" + filePath + "@" + commit, "failed to inject CCS model properly. got %s but wanted %s" % (self.id, gitRepo + "@" + filePath + "@" + commit)
        else:
            assert self.id == gitRepo + "@" + filePath + "@latest", "failed to inject CCS model properly. got %s but wanted %s" % (self.id, gitRepo + "@" + filePath + "@latest")


class BoolAttribute(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "BoolAttribute"
        self.extendsId = "Attribute"
        self.value = None


class ChoiceAttribute(Attribute):
    """ ChoiceAttribute

        Attributes:
            options (list): A dictionary of OptionAttributes
            value (Attribute): The dictionary key of the chosen OptionAttribute from self.options
    """
    def __init__(self):
        super().__init__()
        self.id = "ChoiceAttribute"
        self.extendsId = "Attribute"
        self.options = None  # dictionary of Attribute instances
        self.value = None  # dictionary key of chosen Attribute instance


class OptionAttribute(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "OptionAttribute"
        self.extendsId = "Attribute"


class NumericAttribute(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "NumericAttribute"
        self.extendsId = "Attribute"
        self.value = None
        self.minVal = -inf
        self.maxVal = inf
        self.stepSize = None
        self.makeInt = False
        self.moreIsBetter = True


class PricingModel(ChoiceAttribute):
    def __init__(self):
        super().__init__()
        self.id = "PricingModel"
        self.extendsId = "ChoiceAttribute"
        self.options = {
            "payAndGo": PayAndGo(),
            "subscription": Subscription()
        }
        self.value = None


class PricingModelInterface(OptionAttribute, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def getPrice(self, req, priceFuncs, currencyConversion=1):
        for p in priceFuncs:
            print(p.description, ":", p.run(req) * currencyConversion)
        pass


class PayAndGo(PricingModelInterface):
    def __init__(self):
        super().__init__()
        self.id = "PayAndGo"
        self.extendsId = "OptionAttribute"
        self.description = "you (pay) an upFrontCost once (and go) on to use the service"

        self.upFrontCost = None

    def getPrice(self, req, priceFuncs, currencyConversion=1):
        for p in priceFuncs:
            print(p.description, ":", p.run(req) * currencyConversion)

        self.upFrontCost = sum([pf.run(req) for pf in priceFuncs]) * currencyConversion
        return self.upFrontCost


class Subscription(PricingModelInterface):
    def __init__(self):
        super().__init__()
        self.id = "Subscription"
        self.extendsId = "OptionAttribute"
        self.description = "you pay a billingPeriodCost per billingPeriod. the unit of billingPeriod is per hour"

        self.upfrontCost = 0
        self.billingPeriodCost = None
        self.billingPeriod = None  # per hour

    def getPrice(self, req, priceFuncs, currencyConversion=1):
        self.billingPeriodCost = sum([pf.run(req) for pf in priceFuncs])
        return ((self.billingPeriod * self.billingPeriodCost) + self.upfrontCost) * currencyConversion


class Price(Attribute):
    """ everything to evaluate the final price based on CCS configuration and the pricing model enforced by the CCS """
    def __init__(self):
        super().__init__()
        self.id = "Price"
        self.extendsId = "Attribute"
        self.currency = None  # expecting ISO 4217 currency code as string
        self.priceFuncs = []
        self.model = PricingModel()


# an interface as per https://stackoverflow.com/questions/2124190/how-do-i-implement-interfaces-in-python
class PriceFunc(ABC):
    def __init__(self):
        super().__init__()
        self.description = None

    @abstractmethod
    def run(self, req):
        """ returns the value of this price function """
        pass


def extractConfigurationTree(ccs):
    """ extract the configuration of all CCS and their sub CCS """

    def helper(attr):
        res = {attr.id: {}}
        fields = vars(attr)  # https://stackoverflow.com/a/55320647
        hasAttributes = False
        for key in fields:
            # scan all fields and filter out the attributes
            try:
                if isAncestorOf("Attribute", fields[key].id):
                    # if fields[key] is an attribute ...
                    hasAttributes = True
                    res[attr.id].update(helper(fields[key]))
            except Exception as e:
                #print(e)
                pass

        if not hasAttributes:
            res[attr.id]["value"] = fields["value"]
            res[attr.id]["description"] = fields["description"]

        return res

    return helper(ccs)


def estimatePrice(req, ccs, currency="EUR"):
    """ returns a dict containing the total price and a dict of configurations that it resulted from """

    # get prices of all CCS and their subCCS
    allSubCCSPrices = extractPrices(ccs)

    # convert prices to the same currency
    # TODO inject API key using command line flag or environment variable or config file
    apiKey = "080197719e5c4ef0b73f339e208f1f67"
    # TODO cache this table for at least one day
    ratesRelativeToUSD = json.loads(
        requests.get("https://openexchangerates.org/api/latest.json?app_id=" + apiKey + "&base=USD").content)[
        "rates"]
    currencyConversion = 1
    try:
        currencyConversion = ratesRelativeToUSD[currency]  # how many of requirements currency is 1 USD
    except Exception as e:
        logging.error("your requirement uses a currency with a currency code that does not comply with ISO_4217:",
                      currency)
        print(e)

    try:
        currencyConversion /= ratesRelativeToUSD[ccs.price.currency]  # how many of CCSs currency is 1 USD
    except Exception as e:
        logging.error(ccs.price.id, "uses a currency with a currency code that does not comply with ISO_4217:",
                      ccs.price.currency)
        print(e)

    if ccs.price.model.value is None:
        logging.error(ccs.price.id, "does not provide a pricing model choice")

    totalPrice = {"price": 0, "billingPeriod": "None", "config": extractConfigurationTree(ccs)}

    # get cheapest price of all of the subCCS
    for price in allSubCCSPrices:
        # get cheapest pricing method for this subCCS price and add it to the totalPrice
        cheapestPrice = inf
        for choice in price.model.options:
            curPrice = price.model.options[choice].getPrice(req, price.priceFuncs, currencyConversion=currencyConversion)
            if curPrice < cheapestPrice:
                cheapestPrice = curPrice

            if choice == "subscription":
                totalPrice["billingPeriod"] = price.model.options[choice].billingPeriod

        totalPrice["price"] += cheapestPrice
    return totalPrice


class CCS(Attribute):
    def __init__(self):
        super().__init__()
        self.id = "CCS"
        self.extendsId = "Attribute"

        self.pageUrl = None
        self.price = Price()


class IaaS(CCS):
    def __init__(self):
        super().__init__()
        self.id = "IaaS"
        self.extendsId = "CCS"

        self.region = Region()


class StorageAsAService(IaaS):
    def __init__(self):
        super().__init__()
        self.id = "StorageAsAService"
        self.extendsId = "IaaS"

        self.storage = Storage()
        self.storageWriteSpeed = StorageWriteSpeed()
        self.storageReadSpeed = StorageReadSpeed()


class ServerAsAService(IaaS):
    def __init__(self):
        super().__init__()
        self.id = "ServerAsAService"
        self.extendsId = "IaaS"

        self.operatingSystem = OperatingSystem()
        self.cpuCores = CpuCores()
        self.cpuClockSpeed = CpuClockSpeed()
        self.ram = Ram()
        self.ramClockSpeed = RamClockSpeed()
        self.ramWriteSpeed = RamWriteSpeed()
        self.ramReadSpeed = RamReadSpeed()
        self.storage = Storage()
        self.storageWriteSpeed = StorageWriteSpeed()
        self.storageReadSpeed = StorageReadSpeed()
        self.networkCapacity = NetworkCapacity()
        self.networkUploadSpeed = NetworkUploadSpeed()
        self.networkDownloadSpeed = NetworkDownloadSpeed()


class VMAsAService(ServerAsAService):
    def __init__(self):
        super().__init__()
        self.id = "VMAsAService"
        self.extendsId = "ServerAsAService"


class SaaS(CCS):
    def __init__(self):
        super().__init__()
        self.id = "SaaS"
        self.extendsId = "CCS"


class DatabaseAsAService(SaaS):
    def __init__(self):
        super().__init__()
        self.id = "DatabaseAsAService"
        self.extendsId = "SaaS"


class SQLDatabaseAsAService(DatabaseAsAService):
    def __init__(self):
        super().__init__()
        self.id = "SQLDatabaseAsAService"
        self.extendsId = "DatabaseAsAService"


class NoSQLDatabaseAsAService(DatabaseAsAService):
    def __init__(self):
        super().__init__()
        self.id = "NoSQLDatabaseAsAService"
        self.extendsId = "DatabaseAsAService"


def extractAttributes(attribute):
    """ Recursively get all fields and subfields of an `Attribute` instance that are also of type `Attribute`. Also
        scans the options field of ChoiceAttributes

        Args:
            attribute (Attribute): The CCS of which all fields of type Attribute are to be extracted

        Returns:
            list(Attribute): A list of Attribute instances

        Note:
            CCS also inherits from Attribute
    """
    res = []
    fields = vars(attribute)  # https://stackoverflow.com/a/55320647
    for key in fields:
        try:
            if isAncestorOf("Attribute", fields[key].id):
                res += [fields[key]] + extractAttributes(fields[key])
                if isAncestorOf("ChoiceAttribute", fields[key].id):
                    # also extract all choices of the choiceAttribute and their Attribute type subfields

                    # TODO mark extracted optionattribute subfield as such. only the selected optionattributes of choiceattributes must be considered in matchCCS, otherwise unselected optionattributes will spoof the price estimate
                    res += [fields[key].options[choice] for choice in fields[key].options]
                    for attrs in [extractAttributes(fields[key].options[choice]) for choice in fields[key].options]:
                        res += attrs
        except Exception as e:
            pass
    return res


def extractPrices(attribute):
    """ Recursively get all fields and subfields of an `Attribute` instance that are of type `Price`. Also
        scans the options field of ChoiceAttributes

        Args:
            attribute (Attribute): The CCS of which all fields of type Attribute are to be extracted

        Returns:
            list(Attribute): A list of Attribute instances

        Note:
            CCS also inherits from Attribute
    """
    priceFuncs = []
    attrs = extractAttributes(attribute)
    for attr in attrs:
        if isAncestorOf("Price", attr.id):
            priceFuncs += [attr]

    return priceFuncs


def matchAttribute(ccs, *attributeIds):
    """ Recursively get the first field of type `Attribute` of - either the given `CCS` or one if its subfields of type
       `Attribute` - that are related to the given `attributeIds` in the given order. Options of Attributes of type
       ChoiceAttribute will also be scanned for matches

        Args:
            ccs (CCS): The CCS whose fields will be searched
            attributeIds (tuple(str)): The id that a field of type Attribute should match with

        Returns:
            Attribute: The field that matched with attributeId

        Note:
            CCS also inherits from Attribute

        Example:
            >>> # returns the `storage` field of the VMAsAService instance
            >>> matchAttribute(VMAsAService, "Storage")

            >>> # returns the `storage` field of the StorageAsAService instance inside the VMAsAService instance
            >>> matchAttribute(VMAsAService(), "StorageAsAService", "Storage")

            >>> # returns the VMAsAService instance
            >>> matchAttribute(VMAsAService(), "VMAsAService")
    """

    def matchAttributeHelper(_ccs, *_attributeIds):
        if len(_attributeIds) < 1:
            # done
            return None

        # its the extendsId that has to match because requirements (of type CCS) never have ids that relate to anything
        if isAncestorOf(_ccs.extendsId, _attributeIds[0]):
            if len(_attributeIds) == 1:
                # done
                return _ccs
            # continue search for next attributeId
            return matchAttributeHelper(_ccs, *_attributeIds[1:])

        attributes = extractAttributes(_ccs)

        for attr in attributes:
            if isAncestorOf(attr.id, _attributeIds[0]):
                if len(_attributeIds) == 1:
                    # done
                    return attr
                # continue search for next attributeId
                return matchAttributeHelper(attr, *_attributeIds[1:])

        # no match found
        return None

    match = matchAttributeHelper(ccs, *attributeIds)
    if match is None:
        print("WARNING: your requirements did not match", attributeIds,
              "in that order. for better price estimation, you should set those attributes in that order in your "
              "requirements!")
    return match


def getExtendsId(attributeId):
    """ get the `extendsId` field of a class instance that matches with the given `attributeId`

        Args:
            attributeId (str): id of the Attribute whose extendsId field is sought

        Returns:
            str: extendsId field of the Attribute that matches with the given attributeId

        Note:
            - This function can only be called on Attributes that have already been imported.
            - CCS also inherits from Attribute
    """
    if attributeId in importedClasses:
        return importedClasses[attributeId]["extendsId"]
    return None


def isAncestorOf(rid, cid):
    """ checks if an Attribute is related to another Attribute

        Args:
             rid (str): id of the first Attribute
             cid (str): id for the second Attribute

        Returns:
            bool: True if the Attributes are related, else False

        Note:
            - two Attributes are related if either their ids match or an extendsId of the second attribute in any depth matches with the first attribute
            - CCS also inherits from Attribute
    """
    if rid is None or cid is None:
        return False

    if rid == cid:
        return True

    extendsId = getExtendsId(cid)
    while extendsId is not None:
        if rid == extendsId:
            return True
        extendsId = getExtendsId(extendsId)

    return False


def matchCCS(req, ccs):
    """ check if a requirement matches with a CCS and return a satisfying configuration.

        Args:
            req (CCS): The requirements
            ccs (CCS): The CCS to check for a match

        Returns:
            bool: True if they match, else False
            dict: configuration, None if unsatisfied

        Note:
            - A requirement matches with a CCS if and only if every single Attribute field of the requirement is satisfied through a related Attribute field in the CCS
            - Attribute fields must be unique. Each instance of CCS may not have multiple Attribute fields with the same id
            - If a requirement or a CCS has an Attribute field whose subfields have an Attribute with a duplicate id, then only the first matching Attribute with that id will be considered.
    """

    print("checking", ccs.name, "for potential match")

    # requirement is a custom attribute ... because "@" in req.id
    if "@" in req.id:
        # if the parent of req is not related to ccs, then it does not matter whether their attributes match or not
        if not isAncestorOf(req.extendsId, ccs.id):
            print("requirement is not in any way related to", ccs.id)
            return False, None
    else:
        # requirement is a framework attribute
        if not isAncestorOf(req.id, ccs.id):
            print("requirement is not in any way related to", ccs.id)
            return False, None

    reqAttributes = extractAttributes(req)
    ccsAttributes = extractAttributes(ccs)

    configuration = {}

    # pair-wise compare attributes and check if they match
    for ra in reqAttributes:
        configuration[ra.id] = ra.value

        for ca in ccsAttributes:
            if isAncestorOf(ra.id, ca.id):
                if isAncestorOf("NumericAttribute", ra.id):
                    if ra.value is not None:  # both requirement and CCS set this attribute
                        if not ca.mutable and ca.value is None:
                            print(ra.id, "is set as a requirement, but", ccs.id, "can not set it")
                            return False, None
                        if ca.moreIsBetter:
                            if not ca.mutable:
                                if ra.value > ca.value:  # value is too small and not mutable
                                    print(ra.id, "is too small and cannot be made large enough:", "got", ca.value, "wanted", ra.value)
                                    return False, None
                            if ca.maxVal is not None:
                                if ca.maxVal < ra.value:  # value cannot be made large enough
                                    print(ra.id, "is too small and cannot be made large enough:", "got", ca.maxVal, "wanted", ra.value)
                                    return False, None
                        else:
                            if ra.value < ca.value:  # value is too large and not mutable
                                print(ra.id, "is too large and cannot be made small enough:", "got", ca.value, "wanted", ra.value)
                                return False
                            if ca.minVal is not None:
                                if ca.minVal > ra.value:  # value cannot be made small enough
                                    print(ra.id, "is too large and cannot be made small enough:", "got", ca.minVal, "wanted", ra.value)
                                    return False, None

                    # get configuration
                    if not ca.mutable:
                        configuration[ra.id] = ca.value


                    # ra is satisfied by ca

                elif isAncestorOf("BoolAttribute", ra.id):
                    if not ca.mutable:
                        if ra.value != ca.value:  # value does not match and is not mutable
                            print(ra.id, "does not match and is not mutable:", "wanted", ra.value, "got", ca.value)
                            return False, None

                    # get configuration
                    if not ca.mutable:
                        configuration[ra.id] = ca.value

                    # ra is satisfied by ca

                elif isAncestorOf("ChoiceAttribute", ra.id):
                    if ra.value is not None:
                        if ca.mutable:
                            if not any([isAncestorOf(ra.options[ra.value].id, ca.options[choice].id) for choice in ca.options]):  # value mutable but not available
                                print(ra.id, "option not available:", ra.options[ra.value].id, "not related to any of", [ca.options[choice].id for choice in ca.options])
                                return False, None
                        else:
                            if not isAncestorOf(ra.options[ra.value].id, ca.options[ca.value].id):  # value does not match and is not mutable
                                print(ra.id, "does not match:", ra.options[ra.value].id, "not related to", ca.options[ca.value].id)
                                return False, None

                    # get configuration
                    if not ca.mutable:
                        configuration[ra.id] = ca.value

                    # ra is satisfied by ca

    # req is satisfied by ccs
    return True, configuration


def renderHierarchy():
    """ render the class hierarchy of all imported attributes """

    dot = graphviz.Digraph(comment="Attribute hierarchy", format="svg")
    dot.graph_attr.update({
        "rankdir": "LR"
    })

    def renderFields(d2, attrId):
        glob = globals()
        global importedClasses
        for className in glob:
            # get globally imported classes
            if className == importedClasses[attrId]["className"]:
                vs = vars(glob[className]())
                # get fields of new class instance
                for field in vs:
                    # check if field is an Attribute
                    try:
                        if isAncestorOf("Attribute", vs[field].id):
                            # field edge
                            d2.edge(attrId.replace("https://", "").replace("http://", ""), vs[field].id.replace("https://", "").replace("http://", ""), color="red")
                            renderFields(d2, vs[field].id)
                    except Exception as a:
                        pass

    for attributeId in importedClasses:
        dot2 = graphviz.Digraph(comment=attributeId.replace("https://", "").replace("http://", "") + " fields", format="svg")
        dot2.graph_attr.update({
            "rankdir": "LR"
        })

        # recursively create field edges
        renderFields(dot2, attributeId)

        # render individual attributes/ccs and their class fields and their fields' fields
        dot2.render("docs/renders/" + attributeId.replace("https://", "").replace("http://", ""), view=False)

        # hierarchy edge
        dot.edge(attributeId.replace("https://", "").replace("http://", ""), importedClasses[attributeId]["extendsId"].replace("https://", "").replace("http://", ""), color="black")

    # render the entire attribute/ccs class hierarchy
    dot.render("docs/renders/hierarchy", view=False)


class Region(ChoiceAttribute):
    def __init__(self):
        super().__init__()
        self.id = "Region"
        self.extendsId = "ChoiceAttribute"
        self.description = "The continent in which the CCS resides"

        self.options = {
            "europe": Europe(),
            "northAmerica": NorthAmerica(),
            "southAmerica": SouthAmerica(),
            "eastAsia": EastAsia(),
            "antarctica": Antarctica(),
            "africa": Africa(),
            "australia": Australia()
        }
        self.value = None


class Europe(OptionAttribute):
    def __init__(self):
        super().__init__()
        self.id = "Europe"
        self.extendsId = "OptionAttribute"
        self.name = "Europe"


class NorthAmerica(OptionAttribute):
    def __init__(self):
        super().__init__()
        self.id = "NorthAmerica"
        self.extendsId = "OptionAttribute"
        self.name = "North America"


class SouthAmerica(OptionAttribute):
    def __init__(self):
        super().__init__()
        self.id = "SouthAmerica"
        self.extendsId = "OptionAttribute"
        self.name = "South America"


class EastAsia(OptionAttribute):
    def __init__(self):
        super().__init__()
        self.id = "EastAsia"
        self.extendsId = "OptionAttribute"
        self.name = "East Asia"


class Antarctica(OptionAttribute):
    def __init__(self):
        super().__init__()
        self.id = "Antarctica"
        self.extendsId = "OptionAttribute"
        self.name = "Antarctica"


class Africa(OptionAttribute):
    def __init__(self):
        super().__init__()
        self.id = "Africa"
        self.extendsId = "OptionAttribute"
        self.name = "Africa"


class Australia(OptionAttribute):
    def __init__(self):
        super().__init__()
        self.id = "Australia"
        self.extendsId = "OptionAttribute"
        self.name = "Australia"


class Storage(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "Storage"
        self.extendsId = "NumericAttribute"
        self.description = "Storage amount in GB"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class StorageWriteSpeed(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "StorageWriteSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "Storage write speed in GB/s"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class StorageReadSpeed(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "StorageReadSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "Storage read speed in GB/s"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class OperatingSystem(ChoiceAttribute):
    def __init__(self):
        super().__init__()
        self.id = "OperatingSystem"
        self.extendsId = "ChoiceAttribute"
        self.description = "The operating system a CCS runs on"

        self.options = {
            "linux": Linux(),
            "windows": Windows(),
            "mac": Mac()
        }

        self.value = None


class Linux(OptionAttribute):
    def __init__(self):
        super().__init__()
        self.id = "Linux"
        self.extendsId = "OptionAttribute"
        self.value = "Linux (Unix)"


class Windows(OptionAttribute):
    def __init__(self):
        super().__init__()
        self.id = "Windows"
        self.extendsId = "OptionAttribute"
        self.value = "Windows"


class Mac(OptionAttribute):
    def __init__(self):
        super().__init__()
        self.id = "Mac"
        self.extendsId = "OptionAttribute"
        self.value = "Mac (Unix)"


class CpuCores(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "CpuCores"
        self.extendsId = "NumericAttribute"
        self.description = "The amount of CPU cores"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class CpuClockSpeed(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "CpuClockSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "CPU clock speed in GHz"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class Ram(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "Ram"
        self.extendsId = "NumericAttribute"
        self.description = "The amount of Ram in GB"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class RamClockSpeed(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "RamClockSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "RAM clock speed in GHz"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class RamWriteSpeed(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "RamWriteSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "RAM write speed in GB/s"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class RamReadSpeed(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "RamReadSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "RAM read speed in GB/s"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class NetworkCapacity(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "NetworkCapacity"
        self.extendsId = "NumericAttribute"
        self.description = "Network capacity in GB"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class NetworkUploadSpeed(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "NetworkUploadSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "Network upload speed in GB/s"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True


class NetworkDownloadSpeed(NumericAttribute):
    def __init__(self):
        super().__init__()
        self.id = "NetworkDownloadSpeed"
        self.extendsId = "NumericAttribute"
        self.description = "Network download speed in GB/s"

        self.value = None
        self.makeInt = True
        self.minVal = 0
        self.maxVal = inf
        self.moreIsBetter = True

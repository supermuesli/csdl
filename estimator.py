from csdl import *
from math import inf


def estimate(req: Attribute):
    # mock up database of known ccs
    vm1 = VMAsAService()
    vm1.inject("https://github.com/supermuesli/csdl", "aws/ec2/A1Large.py")
    db = [vm1]

    # for loop and inject attributes and compute prices given the requirement
    smallestPrice = inf
    for ccs in db:
        ccsPrice = ccs.price.get(req)
        ccsCurrency = ccs.price.currency.value
        ccsPricingModel = type(ccs.price.model).__name__
        # TODO take into account pricing model as well
        # TODO take into account currency as well
        # example:
        print(ccs.name + " price: ", ccsPrice, ccsCurrency, "using pricing model:", ccsPricingModel)
        if ccsPrice < smallestPrice:
            smallestPrice = ccsPrice

    # return smallest price of ccs that fits the requirement

    return smallestPrice

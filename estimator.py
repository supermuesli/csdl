from csdl import *
from math import inf


def estimate(req: Attribute):
    # mock up database of all known CCS (in reality this should be fetched from csdlhub.com or something like that)
    vm1 = VMAsAService()
    vm1.inject("https://github.com/supermuesli/csdl", "aws/ec2/A1Large.py")

    ebs1 = StorageAsAService()
    ebs1.inject("https://github.com/supermuesli/csdl", "aws/EBS.py")

    db = [vm1, ebs1]

    # for loop and inject attributes and compute prices given the requirement
    smallestPrice = inf
    cheapestCCS = None
    for ccs in db:
        if matchCCS(req, ccs):
            # get price this CCS using the given requirements as configurations
            ccsPrice = ccs.price.get(req)
            ccsCurrency = ccs.price.currency.value
            ccsPricingModel = type(ccs.price.model).__name__
            # TODO take into account pricing model as well

            # print results
            print(ccs.name + " price: ", ccsPrice, ccsCurrency, "using pricing model:", ccsPricingModel)

            # evaluate
            if ccsPrice < smallestPrice:
                smallestPrice = ccsPrice
                cheapestCCS = ccs

    return cheapestCCS, smallestPrice

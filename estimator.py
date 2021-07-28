from csdl import *
from math import inf


def estimate(req, currency="EUR", usageHours=1):
    """ given some requirements"""

    # mock up database of all known CCS (in reality this should be fetched from csdlhub.com or something like that)
    vm1 = VMAsAService()
    vm1.inject("https://github.com/supermuesli/csdl", "aws/ec2/EC2.py")

    ebs1 = StorageAsAService()
    ebs1.inject("https://github.com/supermuesli/csdl", "aws/EBS.py")

    db = [vm1, ebs1]

    # scan through entire CCS database and find matches
    smallestPrice = inf
    cheapestCCS = None
    print("_"*128)
    for ccs in db:
        # check if the requirements match with the current CCS
        if matchCCS(req, ccs):
            # get price using the given requirements as configurations
            ccsPrice = estimatePrice(req, ccs, currency=currency, usageHours=usageHours)
            ccsPricingModel = ccs.price.model.options[ccs.price.model.choice]

            # print results
            print("found match:", ccs.name)
            print("price: ", ccsPrice, currency, "using pricing model:", ccsPricingModel.id, ":", ccsPricingModel.description)
            print("configuration: ", vars(ccs))

            # evaluate
            if ccsPrice < smallestPrice:
                smallestPrice = ccsPrice
                cheapestCCS = ccs

        print("_"*128)
    return cheapestCCS, smallestPrice

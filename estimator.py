from csdl import *


def estimate(req: Attribute):
    # mock up database of known ccs
    vm1 = VMAsAService()
    vm1.inject("https://github.com/supermuesli/csdl", "aws/ec2/A1Large.py")
    db = [vm1]

    # for loop and inject attributes and compute prices given the requirement
    smallestPrice = -1
    for ccs in db:
        ccsPrice = ccs.price.get(req)
        # TODO take into account pricing model as well
        # TODO take into account currency as well
        # example:
        print("current CCS price: ", ccsPrice, "$ per billing hour")
        if ccsPrice < smallestPrice:
            smallestPrice = ccsPrice

    # return smallest price of ccs that fits the requirement

    return smallestPrice

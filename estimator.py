import pprint

from csdl import *
from math import inf


def estimate(req, currency="EUR", usageHours=1):
    """ given some requirements"""

    # mock up database of all known CCS (in reality this should be fetched from csdlhub.com or something like that)
    vm1 = VMAsAService()
    vm1.inject("https://github.com/supermuesli/csdl", "aws/ec2/EC2.py")

    ebs1 = StorageAsAService()
    ebs1.inject("https://github.com/supermuesli/csdl", "aws/EBS.py")

    s3 = StorageAsAService()
    s3.inject("https://github.com/supermuesli/csdl", "aws/s3/S3.py")

    psql = DatabaseAsAService()
    psql.inject("https://github.com/supermuesli/csdl", "aws/rdsPostgres/Postgresql.py")

    db = [vm1, ebs1, s3, psql]

    # scan through entire CCS database and find matches
    smallestPrice = inf
    print("_"*128)

    priceConfig = None
    for ccs in db:
        # check if the requirements match with the current CCS
        match, conf = matchCCS(req, ccs)
        if match:
            # get price using the given requirements as configurations
            priceConfig = estimatePrice(req, ccs, currency=currency, usageHours=usageHours)
            priceConfig["config"] = conf

            # print results
            print("found match:", ccs.name)
            print("price: ", priceConfig["price"], "per", priceConfig["billingPeriod"], "hours", currency, "using pricing model:")
            print("configuration:")
            pprint.pprint(priceConfig["config"])

            # evaluate
            if priceConfig["price"] < smallestPrice:
                smallestPrice = priceConfig["price"]

        print("_"*128)
    return priceConfig

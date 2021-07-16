from estimator import *
from csdl import *


def main():
    # requirements
    req = VMAsAService()

    # common attribute requirements (fields from hierarchy classes)
    req.ram.value = 16
    req.cpuCores.value = 4
    req.storage.storage.value = 500

    # custom attribute requirements
    req.staticIpAddresses = NumericAttribute()
    req.staticIpAddresses.inject("https://github.com/supermuesli/csdl", "aws/ec2/ElasticIpAmount.py")
    req.staticIpAddresses.value = 5

    # price estimate of cheapest ccs that fits requirements
    estimate(req)


if __name__ == "__main__":
    main()

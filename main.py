from estimator import *
from csdl import *


def main():
    # requirements
    usageHours = 24
    req = VMAsAService()

    # common attribute requirements (fields from hierarchy classes)
    req.ram.value = 16
    req.cpuCores.value = 4
    req.storage.storage.value = 50

    # custom attribute requirements
    req.staticIpAddresses = NumericAttribute()
    req.staticIpAddresses.inject("https://github.com/supermuesli/csdl", "aws/ec2/ElasticIpAmount.py")
    req.staticIpAddresses.value = 5

    # TODO at least 2 more requirement examples with mroe complexity 2 for azure 2 for gcp
    # TODO time interval for estimate function
    # TODO regions
    # TODO staticIps

    # price estimate of cheapest ccs that fits requirements
    estimate(req, usageHours)

    # delete temporary git repositories
    cleanGitCache()


if __name__ == "__main__":
    main()

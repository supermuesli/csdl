from estimator import *
from csdl import *


def main():
    # requirements
    req = VMAsAService()
    req.ram.value = 16
    req.cpuCores.value = 4
    req.storage.storage.value = 50
    req.elasticIpAmount = NumericAttribute()
    req.elasticIpAmount.inject("https://github.com/supermuesli/csdl", "aws/ec2/ElasticIpAmount.py")
    req.elasticIpAmount.value = 5  # duck typing

    # price estimate of cheapest ccs that fits requirements
    print(estimate(req))


if __name__ == "__main__":
    main()

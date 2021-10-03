import sys

from estimator import *
from csdl import *


def main():
    usageHours = 24
    currency = "EUR"

    # user requirements
    req = VMAsAService()
    req.inject("https://github.com/supermuesli/csdl", "examples/Requirement1.py")

    # TODO at least 2 more requirement examples with more complexity 2 for azure 2 for gcp

    # price estimate of cheapest ccs that fits requirements
    priceConfig = estimate(req, currency=currency, usageHours=usageHours)

    # render acquired attribute hierarchy
    renderHierarchy()

    # delete temporary git repositories
    cleanGitCache()


if __name__ == "__main__":
    main()

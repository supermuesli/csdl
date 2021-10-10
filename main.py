import sys

from estimator import *
from csdl import *


def main():
    currency = "USD"

    # user requirements
    req = CCS()
    req.inject("https://github.com/supermuesli/csdl", "examples/Requirement1.py")

    # price estimate of cheapest ccs that fits requirements
    priceConfig = estimate(req, currency=currency)

    # render acquired attribute hierarchy
    renderHierarchy()

    # delete temporary git repositories
    cleanGitCache()


if __name__ == "__main__":
    main()

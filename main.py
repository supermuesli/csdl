import sys

from estimator import *
from csdl import *


def main():
    usageHours = 24

    # user requirements
    req = VMAsAService()
    req.inject("https://github.com/supermuesli/csdl", "examples/Requirement1.py")

    # TODO at least 2 more requirement examples with more complexity 2 for azure 2 for gcp
    # TODO time interval for estimate function
    # TODO hierarchical regions
    # TODO staticIps

    # price estimate of cheapest ccs that fits requirements
    estimate(req, usageHours)

    # render acquired attribute hierarchy
    renderHierarchy()

    # delete temporary git repositories
    cleanGitCache()


if __name__ == "__main__":
    main()

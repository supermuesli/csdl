from estimator import *
from csdl import *


def main():
    # requirements
    usageHours = 24
    req = VMAsAService()
    req.inject("https://github.com/supermuesli", "examples/Requirement1.py")

    # TODO at least 2 more requirement examples with more complexity 2 for azure 2 for gcp
    # TODO time interval for estimate function
    # TODO regions
    # TODO staticIps

    # price estimate of cheapest ccs that fits requirements
    estimate(req, usageHours)

    # delete temporary git repositories
    cleanGitCache()


if __name__ == "__main__":
    main()

from estimator import *
from csdl import *


def main():
    # requirements
    req = VMAsAService()
    req.ram.value = 16
    req.cpuCores.value = 4
    req.storage.storage.value = 50

    # price estimate of cheapest ccs that fits requirements
    print(estimate(req))


if __name__ == "__main__":
    main()

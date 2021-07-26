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

    # montag,dienstag einsenden
    # concept page
    # implementation page: strengths, weaknesses, explain why you made decisions
    # limits dokumentieren
    # how to dokumentieren
    # diskussion/evaluations fragen, bewertungspunkte pros/contras ausdenken
    # (optional) user study: fragebogen ausdenken um implementierung zu evaluieren in bezug auf research question (vergleich mit aws price calculator)
    # conclusion: wie gut habe ich die research questions beantwortet? habe ich sie überhaupt behantwortet? was kann man noch machen?

    # price estimate of cheapest ccs that fits requirements
    estimate(req, currency=currency, usageHours=usageHours)

    # render acquired attribute hierarchy
    renderHierarchy()

    # delete temporary git repositories
    cleanGitCache()


if __name__ == "__main__":
    main()

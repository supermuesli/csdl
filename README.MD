# CSDL Framework

## Caveats/Limitations/TODOS
- **the matching problem**
  - when calling `matchCCS(req, ccs)`, it will be checked whether every attributeId
    in req also exists **in whatever depth** inside ccs, and at the same time is satisfied
    (NumericAttribute, ChoiceAttribute and BoolAttributes have to be satisfied). if the
    check passes, then `True` is returned, else `False`
  - when calling `matchField(req, *attrIds)`, it is expected that neither req 
    nor the CCS in which `matchField` is called have duplicate fields of type Attribute
    with the same id. if a duplicate exists, then it will be ignored and only the first 
    occuring attribute of that id will be considered. for example, a `A1Large` instance 
    a field of type `EBS`. both `A1Large` and `EBS` have the field 
    `region` which is an attribute with the id `Region`. if `matchField` scans a ccs
    for a field of type `Attribute` with the id `Region`, then only the matching field
    of `A1Large` will be returned, since its field appears first in the hierarchy.
  - tell user how well their requirements matched (out of all the attribute fields that
    have been matched) and tell user that adding those fields to their requirement
    makes the price estimation more accurate
- the custom attributes are distributed over git. to prevent a left-pad incident (https://snarky.ca/how-do-you-verify-pypi-can-be-trusted/)
  I should add an option to vendor them. csdfhub.com could also vendor them since all
  git links need to be stored on it anyway. whenever a new git link (attribute) is added
  , csdfhub.com could
- i should publish the csdl package to pip: https://realpython.com/pypi-publish-python-package/#preparing-your-package-for-publication
- add environment variable or command line flag for https://openexchangerates.org/api
  apikey
- i should add error handling/throwing such that the estimator tool can recover from
  invalid models or requirements and also to improve user experience of the framework
- searchTags will be aggregated on csdfhub.com, users can then fulltextsearch for 
  searchTags, and CCS or attributes with chosen searchTags will be displayed
- estimator should be sandboxed in a containerized environment (docker) and firewall
  rules could also be enforced if wanted, however this could limit the price calculation
  of some CCS since they have the full expressiveness of python at their disposal and
  could even make http requests to different services to fetch data for price calculation
  
# Why use git?
- enforces unique ids on attributes, ccs and requirements
- enforces versioning of attributes, ccs and requirements
- enables easy collaboration on attribute and ccs models and requirements
- enforces opensource (private repositories forbidden)
- motivates people to do opensource on github (by collecting stars/reputation)
  - proof: see go modules

# Why not use git?
- distributed dependencies may lead to left-pad-incident
  - solvable by vendoring git repositories with models on a central server (csdfhub.com)
  - solvable in the same way as go modules does it
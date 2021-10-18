# Cloud Service Description Framework

This is the implementation of [this](https://git.rwth-aachen.de/swc-theses/bachelor/ferit-tohidi/thesis) bachelor thesis.

A Python framework with which various cloud services, with various pricing schemes, from various providers can be modeled.

## Usage guide
The general usage workflow is always the same: 
- you pick a cloud service that you want to model
- you read through its attributes and pricing schemes on its website
- for each attribute that does not already exist, you need to create a metamodel
- then you model the cloud service using those attributes
- finally, you model the price
- the framework is best understood by checking out the examples in this repository

### Examples
Lots of examples of cloud service metamodels, attribute metamodels and price models are provided in this repository in the following directories:
- *aws*
- *azure*
- *misc*
- *examples*

### Caveats
- only model per file is allowed
- the model class name must equal filename without *.py* extension
- prices are only expressible per billing period
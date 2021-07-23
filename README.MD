# CSDL Framework

## Caveats/Limitations
- if custom models or custom attributes main classes extend any class other than 
  CCS or Attribute, there might be unexpected behaviour. throw an error for that
- when matching a requirement to a CCS, it is expected that neither requirement 
  nor CCS has duplicate fields of type Attribute with the same id. if a duplicate
  exists, then it will be ignored and only the first occuring attribute of that id
  will be considered in the matching. for example, a `VMAsAService` instance has a field
  `StorageAsAService`. both `VMAsAService` and `StorageAsAService` have the field 
  `region` which is an attribute with the id `Region`. if a requirement sets that 
  region to USA, then both the VMAsAService and the StorageAsAService will
  automatically be expected to have the region set to USA in the matching.
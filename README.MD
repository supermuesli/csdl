# CSDL Framework

## Caveats/Limitations
- if custom models or custom attributes main classes extend any class other than 
  CCS or Attribute, there might be unexpected behaviour. throw an error for that
- when calling `matchField`, it is expected that neither requirement 
  nor CCS have duplicate fields of type Attribute with the same id. if a duplicate
  exists, then it will be ignored and only the first occuring attribute of that id
  will be considered. for example, a `VMAsAService` instance has a field
  of type `StorageAsAService`. both `VMAsAService` and `StorageAsAService` have the field 
  `region` which is an attribute with the id `Region`. if `matchField` scans a ccs
  for a field of type `Attribute` with the id `Region`, then only the matching field
  of `VMAsAService` will be returned, since its field appears first in the hierarchy.
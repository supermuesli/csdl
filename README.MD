# CSDL Framework

## Caveats
- when extending choiceAttributes, the options lists should be concatenated 
  instead of overwritten... maybe
- if custom models or custom attributes main classes extend any class other than 
  CCS or Attribute, there might be unexpected behaviour. throw an error for that
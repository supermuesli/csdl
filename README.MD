# CSDL Framework

## Caveats
- if injected models (.py files) happen to have identical filePath's, meaning their 
  class names are identical, it could lead to accidental overwriting of model classes.
  a solution could be to refactor the injected class names into a random 6-digit 
  random string and store it in a global dictionary
- 
# Abaqus Parser

Abaqus Parser is a Python tool to parse, modify and write abaqus input files.

# Example
```
from abq import inp
content = inp.read_from_file("abaqus_input_file.inp")
inp.write_to_file("modified_abaqus_input_file.inp", content)
```

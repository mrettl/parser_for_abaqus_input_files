[![codecov](https://codecov.io/gh/mrettl/parser_for_abaqus_input_files/branch/main/graph/badge.svg?token=6XJHWS8JHN)](https://codecov.io/gh/mrettl/parser_for_abaqus_input_files)

# Parser for Abaqus input files

This parser is a Python tool to parse and write abaqus input files.
The parsed data are (nested) Python lists, dictionaries, strings, floats and integers.

The parsed input is a list of keyword blocks and comments.

A comment is a string.

A keyword block is a dictionary with keys: values

- keyword: upper case string starting a keyword line. E.g. `ELEMENT` for `*Element, type=C3D4`
- parameters: Dictionary of upper case parameters in the keyword line following the keyword.
  E.g. `{"TYPE": "C3D4"}` for ``*Element, type=C3D4``
- data: List of data lines and comments following the keyword line

A data line is a list of strings or floats or integers. 
E.g. the data line corresponding to `CONSTANT, 23, 1E-6, 0.1`
is `['CONSTANT', 23, 1e-06, 0.1]`.

## Example - 1

Read and write from an abaqus input file:

```python
from abq_parser import inp
content = inp.read_from_file("abaqus_input_file.inp")
inp.write_to_file("modified_abaqus_input_file.inp", content)
```

## Example - 2

Set new coordinates for the first node in the node block.

```python
from abq_parser import inp
content = inp.read_from_string("*Node\n1, 0.0, 0.0, 0.0")
content[0]["data"][0] = [1, 10., 0., 0.]
print(content)
# Prints: 
# [{'keyword': '*NODE', 'parameters': {}, 'data': [[1, 10.0, 0.0, 0.0]]}]

print(inp.write_to_string(content))
# Prints:
# *NODE
# 1, 10.0, 0.0, 0.0
```

## Installation

1. Clone the repository into a folder
2. Open a shell in this folder where the `setup.py` file is located.
   Activate your environment, if you are using conda.
3. Type:


    pip install .


4. To uninstall the package, type:


    pip uninstall abaqus_parser


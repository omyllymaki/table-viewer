# table-viewer

Simple utility program for viewing, filtering, grouping, and sorting of tabular data.

## Usage

Basic usage:

```
python main.py --path path1 path2 path3 
``` 

or simply just

```
python main.py 
``` 

For more detailed usage, see

```
python main.py -h
```

**Queries**


Syntax:

* [col1, col2]: search from col1 and col2.
* &&: logical AND, returns intersection.
* ||: logical OR, returns union.

Example:

[col1, col2] regxp1 && regxp2 || [col3] regexp3

See query_examples.py file for more examples.


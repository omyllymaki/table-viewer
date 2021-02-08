# table-viewer

Simple utility program, with minimal GUI, for viewing, filtering, grouping, and sorting tabular data.

# Usage

## Running program

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

## GUI operations

Left click header: sort by column

Right click header: group by column / reverse grouping

**Search**

Syntax:

- **regxp** : search regexp from all columns.
- **[col1, col2] regxp** : search regexp from columns col1 and col2.
- **&&** : logical AND, returns intersection.
- **||** : logical OR, returns union.

Example:

query = [Lives, Born] tam* || [Nationality] fin

Looks pattern "tam*" from columns [Lives, Born] or pattern "fin" from columns [Nationalioty]; returns union of these. 

See query_examples.py file for more examples.


# datasette-searchable-filter-columns

Type to search the column dropdown in Datasette's table filters.

Datasette's table filter lists every column in one dropdown, which gets
unwieldy on wide tables. This plugin turns that dropdown into a search box:
start typing and the list narrows to matching columns. Columns stay in their
original order, and filters are submitted exactly as before.

## Installation

Install it into the same environment as Datasette:

```bash
datasette install datasette-searchable-filter-columns
```

## Usage

Run Datasette as usual and open any table:

```bash
datasette data.db
```

In the table's filter row, the column selector is now a search box — type part
of a column name to narrow the list, pick one, and add your filter as normal.
It works automatically; there's nothing to configure.

## For developers

Clone this repository and install your local copy in editable mode, so your
edits take effect without reinstalling:

```bash
pip install -e . --no-build-isolation
```

Run the tests:

```bash
python -m unittest discover
```

# datasette-searchable-filter-columns

Datasette plugin that makes the table filter-column dropdown searchable.

Datasette's table filter form uses a native select containing every column in
the table. That can be awkward for wide datasets with dozens of columns. This
plugin adds a small autocomplete input over that select so you can type to
narrow the columns, while preserving the original Datasette form submission
behaviour. It does not reorder the columns — the original column order is kept,
since that order can be meaningful.

## Installation

Install this plugin in the same environment as Datasette:

```bash
datasette install datasette-searchable-filter-columns
```

For local development from this checkout:

```bash
pip install -e . --no-build-isolation
```

## Usage

Run Datasette as normal:

```bash
datasette data.db
```

On table pages, the filter column selector is replaced by a searchable input.
Typing narrows the available column names, and selecting a column updates the
underlying Datasette select used when the filter form is submitted.

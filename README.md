# datasette-searchable-filter-columns

Datasette plugin that makes the table filter-column dropdown searchable.

Datasette's table filter form uses a native select containing every column in
the table. That can be awkward for wide datasets with dozens of columns. This
plugin sorts that select alphanumerically and adds a small autocomplete input
while preserving the original Datasette form submission behaviour.

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

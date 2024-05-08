# Past Perfect

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

An experience on storing events.

## How to use

Create a table in your database:
```sql
CREATE TABLE IF NOT EXISTS event (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    data JSON NOT NULL,
    created_at DATETIME NOT NULL,
    UNIQUE(name, data, created_at)
)
```

## Setup Development Environment

You need the following tools installed on your machine:

- [Poetry](https://python-poetry.org) for Python package management.
- [Poetry Plugin: Export](https://github.com/python-poetry/poetry-plugin-export)
  for exporting dependencies.
- [Poetry Plugin: up](https://github.com/MousaZeidBaker/poetry-plugin-up)
  for updating dependencies.

Ensure you have Python 3.9 or above installed by running:

```bash
python --version
# Python 3.9.x
```

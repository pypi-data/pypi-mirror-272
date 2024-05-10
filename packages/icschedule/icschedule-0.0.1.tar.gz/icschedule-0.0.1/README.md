# icschedule

This project is part of a collection of tools to support running HPC jobs at ICHEC. It provides utilities for working with job schedulers, e.g. Slurm and includes a basic scheduler and collection of mocks to help with submission script prototyping.

# Tests

In a Python virtual environment do:

```sh
pip install .'[test]'
```

## Unit Tests

```sh
pytest
```

## Linting and Static Analysis

```sh
black src test
mypy src test
```

## All Tests

Requires `tox`:

```sh
tox
```


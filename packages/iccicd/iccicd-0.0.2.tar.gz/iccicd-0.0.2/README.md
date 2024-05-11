# iccicd

This project is a collection of utilities for managing project CI/CD pipelines at ICHEC.

# Install

The package is available from PyPi:

```sh
pip install iccicd
```

# CLI

There is a CLI available at `src/iccicd_cli.py` for some operations. Example uses:

## Deploy a Python Package to PyPi

From the packages' top-level directory:

```sh
iccicd_cli deploy --pypi_token $YOUR_PYPI_TOKEN
```

## Increment a Package's Version Number

From the packages' top-level directory:

```sh
iccicd_cli version_bump --version_bump_type minor
```


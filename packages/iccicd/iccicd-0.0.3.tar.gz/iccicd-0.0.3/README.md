# iccicd

This project is a collection of utilities for managing project CI/CD pipelines at ICHEC.

# Install

The package is available from PyPi:

```sh
pip install iccicd
```

or to install from source:

```sh
pip install -e .
```


## Deploy a Python Package to PyPi

From the packages' top-level directory:

```sh
iccicd deploy --pypi_token $YOUR_PYPI_TOKEN
```

## Increment a Package's Version Number

From the packages' top-level directory:

```sh
iccicd version_bump --version_bump_type minor
```


# Pokemon Python API

Simple Python API for connecting to the pokemon REST API. Search for pokemon info by name or ID.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

To write and test code you will need [Python](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/) installed. If your on a Mac, use [Homebrew](https://docs.brew.sh/Installation) for installation.

```shell
brew install python@3.11
brew install poetry
```

### Installing

Install project dependencies

```shell
poetry install
```

## Running the tests

Tests can be run globally from the root directory by running `poetry run pytest`

```shell
poetry run pytest
```

## Built With

### Languages / Core Tools

- [Python3](https://www.python.org/) - The primary language

### Secondary Tooling

- [pytest](https://docs.pytest.org/en/stable/) - Unit testing framework
- [poetry](https://python-poetry.org/) - Python package management
- [fastAPI](https://fastapi.tiangolo.com/) - Web framework for building APIs with Python
- [httpx](https://www.python-httpx.org/) - HTTP client for Python

## Using the App

Change to the root directory and run `poetry start-server`

```shell
poetry start-server
```

## OpenAPI Docs

Once server is running, openAPI and redoc documentation can be accessed via the following URL's:

```
http://<host>:<port>/docs
http://<host>:<port>/redoc
```

## Versioning

There are no particular versioning systems in use.

## Authors

![](docs/mrkiplin-icon.gif)

**Theodore Jones** - [MrKiplin](https://github.com/MrKiplin)

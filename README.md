# Truework Python SDK

A first party Python SDK for the [Truework API](https://www.truework.com/docs/api/).

Code in this repository is licensed under the MIT license, see LICENSE for details.

## Installation

```python
pip install truework
```

PyPI library can be found [here](https://pypi.org/project/truework/)

## Requirements

- python 2.7 or python 3.6+

## Usage

```python
import truework

truework.API_TOKEN = '<your_token>'

# Get the first 10 companies that match the query "International"
truework.Company.search('International', offset=0, limit=10)
```

## Development

First you need to install some additional packages by running
```python
pip install -r requirements-dev.txt -r requirements-test.txt
```
Then to test run:
```
tox
```

This will test the SDK in both `python2` and `python3` environments.


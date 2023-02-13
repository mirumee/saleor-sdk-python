# This repository will be renamed to saleor-sdk-python once it's published

We don't publish repositories, when the time comes the code here will be copied to a new and public repository. This is to prevent leakage of potentially sensitive data that could be contained in issues, pull requests, comments etc.
This is to say one should not rely on the redirection GitHub provides - saleor-sdk-python-private will not redirect to saleor-sdk-python.

# Saleor SDK Python

A set of tools that help Python developers work with Saleor. This is a very early stage in the life of this library and many things are not yet figured out. 

Documentation, contribution rules, process and the code itself (this includes the APIs) are expected to change rapidly.

## Installation

Install [Poetry](https://python-poetry.org/docs/#installing-with-pipx).

Clone the repository and invoke:

```
poetry install
```

## Documentation

In the Poetry shell (`poetry shell` after installing the dependencies), run:

```
mkdocs serve
```

and navigate to http://127.0.0.1:8000

## Tooling

This library provides a CLI that contains a growing set of commands that are useful in day-to-day development around Saleor.

There are two entrypoints (here is a [good article](https://snarky.ca/why-you-should-use-python-m-pip/) on why this is important):

```sh
python -m saleor_sdk tools
saleor_sdk tools
```

### Saleor ID encoding

```sh
saleor-sdk tools decode-id VXNlcjoyMg==
saleor-sdk tools encode-id User 22
```

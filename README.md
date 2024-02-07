# Saleor SDK Python

A set of tools that help Python developers work with Saleor. This is a very early stage in the life of this library and many things are not yet figured out. 

Documentation, contribution rules, process and the code itself (this includes the APIs) are expected to change rapidly.

## Installation

```
pip install saleor-sdk-python
```

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

## Development

To contribute to this repository you will need Hatch to setup a local development environment. 

Install [Hatch](https://hatch.pypa.io/latest/install/#pipx).

### Documentation

1. Run the below command to start a dev server with the documentation site:

```
hatch run docs:serve
```

Dev server provides a live reload on changes and lets you preview the site after it's published



and navigate to http://127.0.0.1:8000

### Tests

To run tests suite use the following command: 

```
hatch run test 
```

### Code style and linters

Use the following commands to format the code and lint it for issues:

```
hatch run lint:fmt
hatch run lint:all
```


### Build and deploy

To publish a new version to PyPI, update it's version number in the `pyproject/toml` file and create new github release.

In case whe you need to make a new release without GitHub workflow, use following `hatch` commands:

```
hatch build -c
hatch publish
```

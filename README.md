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

You can deploy a local documentation service, it reloads changes and allow for a live preview of how the documentation will look like after publication:

```
hatch run docs:serve
```

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

This is done by a CI/CD workflow upon the creation of a release but in case of the need for a manual publication of the packager to PyPI you need to build the package archive and publish it. 

```
hatch build -c
hatch publish
```

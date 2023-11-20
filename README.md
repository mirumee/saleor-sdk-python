# Saleor SDK Python

A set of tools that help Python developers work with Saleor. This is a very early stage in the life of this library and many things are not yet figured out. 

Documentation, contribution rules, process and the code itself (this includes the APIs) are expected to change rapidly.

## Installation

Install [Hatch](https://hatch.pypa.io/latest/install/#pipx).

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

## Documentation

```
hatch run docs:serve
```

and navigate to http://127.0.0.1:8000

## Tests

```
hatch run test 
```

## Build and deploy

```
hatch build -c
hatch publish
```

## Code style

```
hatch run lint:fmt
hatch run lint:all
```

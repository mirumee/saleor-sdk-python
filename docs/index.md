# Introduction

Saleor SDK Python is a Python library that implements tools and solutions useful in Saleor application development, including:

- the `saleor_sdk.crypto` package for working with Saleor's auth.

Before starting, you should familiarize yourself with Saleor's [Extending Saleor](https://docs.saleor.io/docs/3.x/developer/extending/overview) documentation
and learn basic concepts like apps, webhooks and events.


This SDK is framework agnostic. It can be used with any Python web framework, or without framework as part of a script.

## What about the Python App Framework?

The [saleor-app-framework-python](https://github.com/mirumee/saleor-app-framework-python) has been deprecated and is no longer maintained.

## Installation

```
pip install saleor-sdk-python
```

## Key features

- CLI tools automating common development tasks: testing, linting and publication.
- CLI utility for deserializing Saleor's GraphQL IDs values to reveal type names and their database IDs - helpful in debugging and local development.
- 
- Crypto module helping with Saleor authentication, both JWT verification and webhook signature verification - provides a way to manage Saleor issued signatures
- Marina module - more on that in a later time...

## Best served with

- https://ariadnegraphql.org/
- https://github.com/mirumee/ariadne-codegen

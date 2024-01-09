# Introduction

Saleor SDK Python is a Python library which purpose is to contain code that is repeated in different Saleor applications.

You should read [Saleor's Documentation](https://docs.saleor.io/docs/3.x/developer/extending/overview) on the topic to get a grasp on the concepts of the "app framework" Saleor comes with.

This SDK is agnostic of any framework, which makes it possible to use in all sorts of web (or otherwise) frameworks and even scripts.

## What about Python App Framework?

The old [saleor-app-framework-python](https://github.com/mirumee/saleor-app-framework-python) was very opinionated on how an application should be crated. It required FastAPI and in a specific version of it.  

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

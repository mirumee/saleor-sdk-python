# Simple FastAPI Example

The following is a single module FastAPI app written as a demo of the Saleor SDK Python package.
This **should not** be treated as a production ready application.

For the sake of time let's import everything that will be needed upfront, initialize the app and put a JWKS storage in place:

```python
{!./docs/examples/simple/app.py[ln:1-18]!}
```

## Declare the App manifest

```python hl_lines="7 8 13 14"
{!./docs/examples/simple/app.py[ln:20-39]!}
```

There are a few things to notice here:

- **enums** - the SDK will try to keep the definitions up-to-date with Saleor but there is no promise this will always meet your needs (time-wise), this is why you can use both, the definitions from `saleor_sdk.schemas.enums` and plain strings.
- **`request.url_for()`** - Saleor needs a full URL to your endpoint, here we leverage FastAPI's resolver (be mindful about what your proxy is doing, i.e. it's easy to hide crucial information from FastAPI with Gunicorn)
- **Subscription queries** - the payload that webhook is to carry.

### More on Subscription queries

Since Saleor 3.2 (and 3.6 for synchronous events) one can define the payload that Saleor will send to an app - this allows you to define a payload that is meaningful to the app. 

[Saleor docs: Subscription Webhook Payloads](https://docs.saleor.io/docs/3.x/developer/extending/apps/subscription-webhook-payloads)

A formatted query from the example looks like this:

```graphql
subscription {
  event {
    issuedAt
    issuingPrincipal {
      ... on App {
        id
      }
      ... on User {
        id
      }
    }
    ... on OrderCreated {
      order {
        id
      }
    }
    ... on OrderUpdated {
      order {
        id
      }
    }
  }
}
```

and will result in the following payload being sent to the app:

```json
{
    "issuedAt": "2022-12-12T00:37:17.405467+00:00",
    "issuingPrincipal": {
        "id": "VXNlcjoyMDU5ODA1MTg0"
    },
    "order": {
        "id": "T3JkZXI6MWFkNzZjOTctZDkxNy00NjRmLWIwNzUtOTljNzcwY2IzOWI4"
    }
}
```

## Define some commonly used dependencies

```python
{!./docs/examples/simple/app.py[ln:42-53]!}
```

## JWKS and user JWT verification

There are currently two ways to verify the authenticity of a Saleor issued JWT:
- online - by calling Saleor to check (deprecated by Saleor)
- offline - by checking with Saleor's public keyset.
This library only supports the offline method.

Saleor instances expose a `/.well-known/jwks.json` endpoint which exposes the public part of the RSA key used to sign the JWTs.
With that we can verify if the incoming token is indeed coming straight from Saleor and if we can trust it's claims.

To do that we need a storage within the app's memory to hold on to the JWKS (JSON Web Key Set), in this example we are simply using a global variable.

The `get_saleor_user` dependency ensures the JWKS was initialized (first request in the runtime), then validates the token. If the local JWKS is missing a key, a `JWKSKeyMissing` error will be raised and an attempt to get a fresh one from Saleor will be made - this might happen when Saleor rotates the keys and starts signing JWTs with the new key.

```python
{!./docs/examples/simple/app.py[ln:56-83]!}
```

Here's how it roughly works in sequence

``` mermaid
sequenceDiagram
    actor USR as User
    participant SAL as Saleor
    participant APP as App
    participant STO as JWKS Storage

    USR ->> SAL: Here are my credentials, give me a JWT
    SAL ->> USR: Here's your JWT

    USR ->> APP: Give me that secret resource
    APP ->> STO: I've got a JWT with kid=1 do you have something on that?
    alt Storage does not have the kid=1
        STO ->> APP: No I don't
        APP ->> SAL: Fetch JWKS
        SAL ->> APP: JWKS
        APP ->> STO: Save JWKS
    else
        STO ->> APP: Yes, here is the public key
    end
    APP ->> APP: Verify the JWT signature
    APP ->> USR: Here's the data
```

## Webhook signature verification

A very similar process applies to webhook authenticity verification. Leveraging the public key pair issued by Saleor the signature of a JWS (a JWT with detached payload) that is sent with a webhook can be verified in an offline manner.

```python
{!./docs/examples/simple/app.py[ln:86-109]!}
```

## Finally define the app endpoints

You need the two endpoints required by Saleor's framework:

```python
{!./docs/examples/simple/app.py[ln:112-119]!}
```

- `app_config` - this is the endpoint that is expected to respond with HTML that will initialize a React App in the Saleor Dashboard (read more on [@saleor/app-sdk](https://github.com/saleor/saleor-app-sdk))
- `register` - this endpoint receives the app_token which needs to be persisted securely, it's used by the app to authenticate with Saleor

Further we define the order webhook handler which leverages our `verify_webhook_signature` dependency.

```python
{!./docs/examples/simple/app.py[ln:122-130]!}
```

And an additional endpoint that could be used by the Dashboard UI to for example change the app configuration

```python
{!./docs/examples/simple/app.py[ln:134-137]!}
```

## Running the complete example

Install the `examples` dependencies with:

```
hatch -e examples shell
```

Then navigate to the example and run it with uvicorn:

```
cd docs/examples/simple
uvicorn app:app --reload
```

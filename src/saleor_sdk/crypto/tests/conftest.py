import json

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.algorithms import RSAAlgorithm
from jwt.api_jwk import PyJWKSet

from saleor_sdk.crypto.utils import jws_global_obj, jwt_global_obj


@pytest.fixture(scope="session")
def private_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture(scope="session")
def public_key(private_key):
    return private_key.public_key()


@pytest.fixture(scope="session")
def jwks(public_key):
    jwk_dict = json.loads(RSAAlgorithm.to_jwk(public_key))
    jwk_dict.update({"use": "sig", "kid": "1"})
    return PyJWKSet.from_dict({"keys": [jwk_dict]})


@pytest.fixture(scope="session")
def bad_jwks():
    return PyJWKSet.from_dict({"keys": []})


@pytest.fixture(scope="function")
def webhook_payload():
    return json.dumps({"example": "webhook"})


@pytest.fixture(scope="function")
def webhook_signature(private_key, webhook_payload):
    """
    Based on how Saleor does it
    https://github.com/saleor/saleor/blob/3.9.3/saleor/core/jwt_manager.py#L144-L152
    """
    return jws_global_obj.encode(
        webhook_payload.encode("utf-8"),
        key=private_key,
        algorithm="RS256",
        headers={"kid": "1"},
        is_payload_detached=True,
    )


@pytest.fixture(scope="function")
def principal_jwt(private_key):
    """
    Based on how Saleor does it
    https://github.com/saleor/saleor/blob/3.9.3/saleor/core/jwt_manager.py#L138-L142
    """
    return jwt_global_obj.encode(
        {
            "owner": "saleor",
            "iss": "https://example.eu.saleor.cloud/graphql/",
            "token": "xxx",
            "email": "pawel.kucmus@mirumee.com",
            "type": "access",
            "user_id": "VXNlcjoyMg==",
            "is_staff": True,
        },
        key=private_key,
        algorithm="RS256",
        headers={"kid": "1"},
    )

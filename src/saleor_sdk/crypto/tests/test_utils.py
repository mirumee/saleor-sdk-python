import json

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.exceptions import InvalidSignatureError

from saleor_sdk.crypto.exceptions import JWKSKeyMissing
from saleor_sdk.crypto.utils import (
    get_key_from_jwks,
    jwt_global_obj,
    decode_jwt,
    decode_webook_payload,
)


def test_get_key_from_jwks(jwks, public_key):
    key = get_key_from_jwks(kid="1", jwks=jwks)
    assert public_key.public_numbers() == key.public_numbers()


def test_get_missing_key_from_jwks(jwks):
    with pytest.raises(JWKSKeyMissing) as excinfo:
        get_key_from_jwks(kid="2", jwks=jwks)
    assert str(excinfo.value) == "The JWKS does not hold the key: 2"


def test_decode_webook_payload(webhook_payload, jwks, webhook_signature):
    decode_webook_payload(
        jws=webhook_signature,
        jwks=jwks,
        webhook_payload=webhook_payload.encode("utf-8"),
    )


def test_decode_webook_payload_verification_failure(jwks, webhook_signature):
    with pytest.raises(InvalidSignatureError):
        decode_webook_payload(
            jws=webhook_signature,
            jwks=jwks,
            webhook_payload=json.dumps({"bad": "webhook"}).encode("utf-8"),
        )


def test_decode_jwt(jwks, principal_jwt):
    decode_jwt(
        jwt=principal_jwt,
        jwks=jwks,
    )


def test_decode_jwt_verification_failure(jwks):
    bad_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    jwt = jwt_global_obj.encode(
        {
            "owner": "saleor",
            "iss": "https://bad.eu.saleor.cloud/graphql/",
            "token": "xxx",
            "email": "bad@mirumee.com",
            "type": "bad",
            "user_id": "VXNlcjoyMg==",
            "is_staff": True,
        },
        key=bad_private_key,
        algorithm="RS256",
        headers={"kid": "1"},
    )

    with pytest.raises(InvalidSignatureError):
        decode_jwt(
            jwt=jwt,
            jwks=jwks,
        )

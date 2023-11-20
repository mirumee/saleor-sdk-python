import json

import jwt
import pytest

from saleor_sdk.crypto.exceptions import JWKSKeyMissing
from saleor_sdk.marina.auth import decode_saleor_jwt, verify_webhook_signature
from saleor_sdk.marina.exceptions import Unauthorized


async def test_decode_saleor_jwt(fake_saleor_jwt, fake_jwks_provider, fake_saleor_jwt_payload):
    payload = await decode_saleor_jwt(jwt=fake_saleor_jwt, jwks_provider=fake_jwks_provider)
    assert payload["token"] == fake_saleor_jwt_payload["token"]
    assert payload["email"] == fake_saleor_jwt_payload["email"]
    assert payload["is_staff"] == fake_saleor_jwt_payload["is_staff"]
    assert payload["user_id"] == fake_saleor_jwt_payload["user_id"]


async def test_decode_saleor_jwt_jwk_missing(mocker, fake_saleor_jwt, fake_jwks_provider, fake_saleor_jwt_payload):
    mock_decode_jwt = mocker.patch("saleor_sdk.marina.auth.decode_jwt")
    mock_decode_jwt.side_effect = [JWKSKeyMissing, fake_saleor_jwt_payload]
    payload = await decode_saleor_jwt(jwt=fake_saleor_jwt, jwks_provider=fake_jwks_provider)
    assert payload == fake_saleor_jwt_payload


async def test_decode_saleor_jwt_invalid(mocker, fake_saleor_jwt, fake_jwks_provider):
    mock_decode_jwt = mocker.patch("saleor_sdk.marina.auth.decode_jwt")
    mock_decode_jwt.side_effect = [
        jwt.InvalidTokenError,
    ]
    with pytest.raises(Unauthorized):
        await decode_saleor_jwt(jwt=fake_saleor_jwt, jwks_provider=fake_jwks_provider)


async def test_verify_webhook_signature(fake_payload_signature, fake_webhook_payload, fake_jwks_provider, issuer):
    await verify_webhook_signature(
        payload=json.dumps(fake_webhook_payload).encode(),
        jws=fake_payload_signature,
        issuer=issuer,
        jwks_provider=fake_jwks_provider,
    )


async def test_verify_webhook_signature_suspicious_payload(fake_payload_signature, fake_jwks_provider, issuer):
    with pytest.raises(jwt.InvalidSignatureError):
        await verify_webhook_signature(
            payload=json.dumps({"if any one asks this order is": "PAID :}"}).encode(),
            jws=fake_payload_signature,
            issuer=issuer,
            jwks_provider=fake_jwks_provider,
        )

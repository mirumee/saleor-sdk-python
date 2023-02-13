from typing import Dict

from jwt.api_jwk import PyJWKSet
from jwt.api_jws import PyJWS
from jwt.api_jwt import PyJWT

from saleor_sdk.crypto.exceptions import JWKSKeyMissing, KeyIDMissing

jwt_global_obj = PyJWT(options={"verify_signature": True})
jws_global_obj = PyJWS(options={"verify_signature": True})
get_unverified_header = jws_global_obj.get_unverified_header


def get_kid(sig_header: Dict[str, str]):
    try:
        return sig_header["kid"]
    except KeyError:
        raise KeyIDMissing()


def get_key_from_jwks(kid: str, jwks: PyJWKSet):
    try:
        jwks_key = jwks[kid]
    except KeyError:
        raise JWKSKeyMissing(f"The JWKS does not hold the key: {kid}")
    return jwks_key.key


def decode_webook_payload(jws: str, jwks: PyJWKSet, webhook_payload: bytes):
    """
    Reads the signature to learn about the incoming JWS (payloadless JWT). Then
    searches for the corresponding key in a JWKS storage. Will throw an
    exception if a key is missing. Finally verifies the payload by decoding it.
    """
    sig_header = get_unverified_header(jws)
    key = get_key_from_jwks(kid=get_kid(sig_header), jwks=jwks)

    return jws_global_obj.decode(
        jws,
        algorithms=[sig_header["alg"]],
        key=key,
        detached_payload=webhook_payload,
    )


def decode_jwt(jwt: str, jwks: PyJWKSet):
    """
    Reads the signature to learn about the incoming JWT. Looks up the key
    by kid. Will throw an exception if a key is missing. Finally verifies the
    payload by decoding it.
    """
    sig_header = get_unverified_header(jwt)
    key = get_key_from_jwks(kid=get_kid(sig_header), jwks=jwks)

    return jwt_global_obj.decode(
        jwt,
        algorithms=[sig_header["alg"]],
        key=key,
    )

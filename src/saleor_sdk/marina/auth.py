from typing import Any

from jwt import decode as jwt_decode
from jwt.exceptions import InvalidTokenError

from saleor_sdk.crypto.exceptions import JWKSKeyMissing
from saleor_sdk.crypto.utils import decode_jwt, decode_webook_payload
from saleor_sdk.marina.exceptions import Unauthorized
from saleor_sdk.marina.jwks import AbstractJWKSProvider


async def decode_saleor_jwt(
    jwt: str,
    jwks_provider: AbstractJWKSProvider,
    force_refresh: bool = False,
) -> Any:
    unverified_paylod = jwt_decode(jwt=jwt, options={"verify_signature": False})
    saleor_jwks = await jwks_provider.get(issuer=unverified_paylod["iss"], force_refresh=force_refresh)

    try:
        return decode_jwt(
            jwt=jwt,
            jwks=saleor_jwks,
        )
    except JWKSKeyMissing:
        if not force_refresh:
            return await decode_saleor_jwt(jwt=jwt, jwks_provider=jwks_provider, force_refresh=True)
    except InvalidTokenError as err:
        raise Unauthorized() from err


async def verify_webhook_signature(
    payload: bytes,
    jws: str,
    issuer: str,  # comes from Saleor-Api-Url header and its the same as iss in JWT
    jwks_provider: AbstractJWKSProvider,
    force_refresh: bool = False,
) -> Any:
    saleor_jwks = await jwks_provider.get(issuer=issuer, force_refresh=force_refresh)

    try:
        return decode_webook_payload(
            jws=jws,
            jwks=saleor_jwks,
            webhook_payload=payload,
        )
    except JWKSKeyMissing:
        if not force_refresh:
            return await verify_webhook_signature(
                payload=payload, jws=jws, issuer=issuer, jwks_provider=jwks_provider, force_refresh=True
            )

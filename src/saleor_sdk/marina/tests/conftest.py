import datetime
import json

import jwt
import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.algorithms import RSAAlgorithm
from jwt.api_jwk import PyJWKSet

from saleor_sdk.marina.client import AbstractSaleorClient
from saleor_sdk.marina.config import AbstractSaleorConfigProvider, SaleorConfigData
from saleor_sdk.marina.jwks import AbstractJWKSClient, AbstractJWKSProvider


@pytest.fixture(scope="session")
def issuer():
    return "https://marina.eu.saleor.cloud/graphql/"


@pytest.fixture(scope="session")
def kid():
    return "1"


@pytest.fixture(scope="session")
def private_key():
    return rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)


@pytest.fixture(scope="session")
def public_key(private_key):
    return private_key.public_key()


@pytest.fixture(scope="session")
def fake_jwks(public_key, kid):
    jwk = RSAAlgorithm.to_jwk(public_key, as_dict=True)
    jwk.update({"use": "sig", "kid": kid})
    return {"keys": [jwk]}


@pytest.fixture()
def fake_saleor_jwt_payload(issuer):
    utcnow = datetime.datetime.now(datetime.timezone.utc)
    return {
        "iat": utcnow,
        "owner": "saleor",
        "iss": issuer,
        "exp": utcnow + datetime.timedelta(seconds=3600),
        "token": "FAKE",
        "email": "marina@mirumee.com",
        "type": "access",
        "user_id": "FAKE==",
        "is_staff": True,
    }


@pytest.fixture()
def fake_saleor_jwt(fake_saleor_jwt_payload, private_key, kid):
    return jwt.encode(
        payload=fake_saleor_jwt_payload,
        key=private_key,
        algorithm="RS256",
        headers={"kid": kid},
    )


@pytest.fixture(scope="session")
def fake_jwks_service(fake_jwks):
    class FakeJWKSService(AbstractJWKSClient):
        async def fetch_jwks(self) -> str:
            return json.dumps(fake_jwks)

    return FakeJWKSService()


@pytest.fixture(scope="session")
def fake_jwks_provider(fake_jwks_service):
    class FakeJWKSProvider(AbstractJWKSProvider):
        def __init__(self, jwks_service: AbstractJWKSClient):
            super().__init__(jwks_service)
            self.jwks_cache = {}

        async def get(self, issuer: str, force_refresh: bool = False) -> PyJWKSet:
            if issuer not in self.jwks_cache or force_refresh:
                await self.set(issuer, await self.jwks_service.fetch_jwks())
            return PyJWKSet.from_json(self.jwks_cache[issuer])

        async def set(self, issuer: str, jwks: str) -> None:
            self.jwks_cache = {issuer: jwks}

    return FakeJWKSProvider(fake_jwks_service)


@pytest.fixture()
def saleor_config():
    return SaleorConfigData(
        saleor_domain="marina.eu.saleor.cloud",
        saleor_app_id="TEST==",
        auth_token="test",
    )


@pytest.fixture()
def fake_saleor_config_provider(saleor_config):
    class FakeSaleorConfigProvider(AbstractSaleorConfigProvider):
        def __init__(self):
            self.saleor_config = saleor_config

        async def get_by_saleor_domain(self, saleor_domain: str) -> SaleorConfigData:
            return self.saleor_config

        async def get_by_saleor_app_id(self, saleor_domain: str) -> SaleorConfigData:
            return self.saleor_config

        async def create_or_update(self, auth_token: str, saleor_domain: str, saleor_app_id: str) -> SaleorConfigData:
            self.saleor_config = SaleorConfigData(
                auth_token=auth_token,
                saleor_domain=saleor_domain,
                saleor_app_id=saleor_app_id,
            )
            return self.saleor_config

    return FakeSaleorConfigProvider()


@pytest.fixture()
def fake_saleor_client():
    class FakeSaleorClient(AbstractSaleorClient):
        async def get_app_id(self, auth_token: str) -> str | None:
            return "APP_ID=="

    return FakeSaleorClient()


@pytest.fixture()
def fake_webhook_payload():
    return {"look_mom": "i'm a payload!"}


@pytest.fixture()
def fake_payload_signature(fake_webhook_payload, private_key, kid):
    return jwt.PyJWS().encode(
        payload=json.dumps(fake_webhook_payload).encode(),
        key=private_key,
        algorithm="RS256",
        headers={"kid": kid},
        is_payload_detached=True,
    )

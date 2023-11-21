import abc

from jwt.api_jwk import PyJWKSet


class AbstractJWKSClient(abc.ABC):
    @abc.abstractmethod
    async def fetch_jwks(self) -> str:
        """Fetch the JWKS from server and return a JSON string containing the JWKS"""


class AbstractJWKSProvider(abc.ABC):
    @abc.abstractmethod
    def __init__(self, jwks_service: AbstractJWKSClient):
        self.jwks_service = jwks_service

    @abc.abstractmethod
    async def get(self, issuer: str, force_refresh: bool = False) -> PyJWKSet:
        """Retrieve the JWKS, needs to call `set` when force_refres is True"""

    @abc.abstractmethod
    async def set(
        self,
        issuer: str,
        jwks: str,
    ) -> None:
        """Set JWKS value in cache for a given issuer."""

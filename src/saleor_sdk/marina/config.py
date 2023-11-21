import abc
from dataclasses import dataclass


@dataclass
class SaleorConfigData:
    saleor_domain: str
    saleor_app_id: str
    auth_token: str


class AbstractSaleorConfigProvider(abc.ABC):
    @abc.abstractmethod
    async def get_by_saleor_domain(
        self,
        saleor_domain: str,
    ) -> SaleorConfigData:
        """Return SaleorConfig for a given Saleor domain"""

    @abc.abstractmethod
    async def get_by_saleor_app_id(
        self,
        saleor_domain: str,
    ) -> SaleorConfigData:
        """Return SaleorConfig for a given Saleor App ID"""

    @abc.abstractmethod
    async def create_or_update(
        self,
        auth_token: str,
        saleor_domain: str,
        saleor_app_id: str,
    ) -> SaleorConfigData:
        """Creates or updates SaleorConfig"""

import logging

from saleor_sdk.marina.client import AbstractSaleorClient
from saleor_sdk.marina.config import AbstractSaleorConfigProvider
from saleor_sdk.marina.exceptions import SaleorAppInstallationProblem
from saleor_sdk.marina.jwks import AbstractJWKSProvider

LOGGER = logging.getLogger(__name__)


async def install_app(
    config_provider: AbstractSaleorConfigProvider,
    jwks_provider: AbstractJWKSProvider,
    saleor_client: AbstractSaleorClient,
    saleor_domain: str,
    saleor_url: str,
    saleor_auth_token: str,
) -> None:
    app_id = await saleor_client.get_app_id(auth_token=saleor_auth_token)

    if app_id is None:
        raise SaleorAppInstallationProblem("Application not available")

    await config_provider.create_or_update(
        auth_token=saleor_auth_token,
        saleor_domain=saleor_domain,
        saleor_app_id=app_id,
    )

    await jwks_provider.get(issuer=saleor_url, force_refresh=True)

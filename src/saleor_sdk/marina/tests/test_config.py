from dataclasses import asdict

from saleor_sdk.marina.config import SaleorConfigData


def test_SaleorConfigData(saleor_config: SaleorConfigData):
    assert asdict(saleor_config) == {
        "saleor_domain": "marina.eu.saleor.cloud",
        "saleor_app_id": "TEST==",
        "auth_token": "test",
    }

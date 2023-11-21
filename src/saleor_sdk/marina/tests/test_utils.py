from saleor_sdk.marina.utils import get_saleor_app_identifier


def test_get_saleor_app_identifier():
    assert get_saleor_app_identifier("DEV", "test_app") == "DEV.test_app"

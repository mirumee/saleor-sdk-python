from saleor_sdk.marina.install import install_app


async def test_install_app(
    fake_saleor_client,
    fake_saleor_config_provider,
    fake_jwks_provider,
):
    await install_app(
        config_provider=fake_saleor_config_provider,
        jwks_provider=fake_jwks_provider,
        saleor_client=fake_saleor_client,
        saleor_domain="marina.eu.saleor.cloud",
        saleor_url="https://marina.eu.saleor.cloud",
        saleor_auth_token="test_token",
    )

    assert fake_saleor_config_provider.saleor_config.auth_token == "test_token"
    assert fake_saleor_config_provider.saleor_config.saleor_app_id == "APP_ID=="

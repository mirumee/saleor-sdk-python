from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field

from saleor_sdk.schemas.enums import (
    MountType,
    Permission,
    TargetType,
    WebhookAsyncEvents,
    WebhookSyncEvents,
)


class Extension(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    label: str
    mount: str | MountType
    target: str | TargetType
    permissions: list[str]
    url: AnyHttpUrl


class Webhook(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    async_events: list[str | WebhookAsyncEvents] | None = Field(default_factory=list, alias="asyncEvents")
    sync_events: list[str | WebhookSyncEvents] | None = Field(default_factory=list, alias="syncEvents")
    query: str
    target_url: AnyHttpUrl = Field(..., alias="targetUrl")
    is_active: bool = Field(..., alias="isActive")


class Manifest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    version: str
    name: str
    about: str | None = None

    permissions: list[str | Permission]

    app_url: AnyHttpUrl = Field(..., alias="appUrl")
    configuration_url: AnyHttpUrl | None = Field(
        None,
        alias="configurationUrl",
        json_schema_extra={"deprecated": True},
    )
    token_target_url: AnyHttpUrl = Field(..., alias="tokenTargetUrl")

    data_privacy: str | None = Field(None, alias="dataPrivacy", json_schema_extra={"deprecated": True})
    data_privacy_url: AnyHttpUrl | None = Field(None, alias="dataPrivacyUrl")
    homepage_url: AnyHttpUrl | None = Field(None, alias="homepageUrl")
    support_url: AnyHttpUrl | None = Field(None, alias="supportUrl")

    extensions: list[Extension] | None = Field(default_factory=list)
    webhooks: list[Webhook] | None = Field(default_factory=list)

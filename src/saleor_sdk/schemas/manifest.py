from typing import List, Union, Optional

from pydantic import BaseModel, Field, AnyHttpUrl, ConfigDict

from saleor_sdk.schemas.enums import (
    Permission,
    MountType,
    TargetType,
    WebhookAsyncEvents,
    WebhookSyncEvents,
)


class Extension(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    label: str
    mount: Union[str, MountType]
    target: Union[str, TargetType]
    permissions: List[str]
    url: AnyHttpUrl


class Webhook(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    async_events: Optional[List[Union[str, WebhookAsyncEvents]]] = Field(default_factory=list, alias="asyncEvents")
    sync_events: Optional[List[Union[str, WebhookSyncEvents]]] = Field(default_factory=list, alias="syncEvents")
    query: str
    target_url: AnyHttpUrl = Field(..., alias="targetUrl")
    is_active: bool = Field(..., alias="isActive")



class Manifest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    version: str
    name: str
    about: Optional[str]

    permissions: List[Union[str, Permission]]

    app_url: AnyHttpUrl = Field(..., alias="appUrl")
    configuration_url: Optional[AnyHttpUrl] = Field(
        None,
        alias="configurationUrl",
        deprecated=True,
    )
    token_target_url: AnyHttpUrl = Field(..., alias="tokenTargetUrl")

    data_privacy: Optional[str] = Field(None, alias="dataPrivacy", deprecated=True)
    data_privacy_url: Optional[AnyHttpUrl] = Field(None, alias="dataPrivacyUrl")
    homepage_url: Optional[AnyHttpUrl] = Field(None, alias="homepageUrl")
    support_url: Optional[AnyHttpUrl] = Field(None, alias="supportUrl")

    extensions: Optional[List[Extension]] = Field(default_factory=list)
    webhooks: Optional[List[Webhook]] = Field(default_factory=list)

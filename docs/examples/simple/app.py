from fastapi import FastAPI, Request, Depends, Header
from pydantic import BaseSettings
import httpx
from jwt.api_jwk import PyJWKSet

from saleor_sdk.schemas.manifest import Manifest, Webhook
from saleor_sdk.schemas.enums import Permission, WebhookAsyncEvents
from saleor_sdk.crypto.utils import decode_webook_payload, decode_jwt
from saleor_sdk.crypto.exceptions import JWKSKeyMissing


class Settings(BaseSettings):
    debug: bool = False

settings = Settings(debug=True)

app = FastAPI(debug=settings.debug)
saleor_jwks = None


@app.get("/api/manifest")
async def manifest(request: Request):
    return Manifest(
        id="simple-sdk-test-app",
        version="0.0.0",
        name="Simple SDK Test APP",
        permissions=[Permission.MANAGE_ORDERS, "MANAGE_CHECKOUTS"],
        app_url=request.url_for("app_config"),
        token_target_url=request.url_for("register"),
        webhooks=[
            Webhook(
                name="Order Handler",
                async_events=[WebhookAsyncEvents.ORDER_CREATED, "ORDER_UPDATED"],
                query="subscription { event { issuedAt issuingPrincipal { ... on App { id } ... on User { id } } ... on OrderCreated { order { id }} ... on OrderUpdated { order { id }}}}",
                target_url=request.url_for("order_handler"),
                is_active=True,
            )
        ],
    )


async def get_saleor_event(saleor_event: str = Header(..., alias="Saleor-Event")):
    return saleor_event


async def get_saleor_domain(saleor_domain: str = Header(..., alias="Saleor-Domain")):
    return saleor_domain


async def get_saleor_signature(
    saleor_signature: str = Header(..., alias="Saleor-Signature")
):
    return saleor_signature


async def fetch_jwks(saleor_domain):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://{saleor_domain}/.well-known/jwks.json")
        return response.content


async def get_saleor_user(
    saleor_domain: str = Depends(get_saleor_domain),
    saleor_token: str = Header(..., alias="Saleor-Token"),
):
    global saleor_jwks
    if not saleor_jwks:
        saleor_jwks = PyJWKSet.from_json(await fetch_jwks(saleor_domain))

    max_attempts = 1

    while max_attempts:
        try:
            return decode_jwt(
                jwt=saleor_token,
                jwks=saleor_jwks,
            )
        except JWKSKeyMissing as exc:
            if max_attempts:
                saleor_jwks = PyJWKSet.from_json(await fetch_jwks(saleor_domain))
                max_attempts -= 1
            else:
                raise


async def verify_webhook_signature(
    request: Request,
    saleor_domain: str = Depends(get_saleor_domain),
    jws: str = Depends(get_saleor_signature),
):
    global saleor_jwks
    if not saleor_jwks:
        saleor_jwks = PyJWKSet.from_json(await fetch_jwks(saleor_domain))

    max_attempts = 1

    while max_attempts:
        try:
            return decode_webook_payload(
                jws=jws,
                jwks=saleor_jwks,
                webhook_payload=await request.body(),
            )
        except JWKSKeyMissing as exc:
            if max_attempts:
                saleor_jwks = PyJWKSet.from_json(await fetch_jwks(saleor_domain))
                max_attempts -= 1
            else:
                raise


@app.get("/", name="app_config")
async def app_config():
    return "OK"


@app.post("/api/register", name="register")
async def register():
    return "OK"


@app.post("/api/webhook/order", name="order_handler")
async def order_handler(
    request: Request, 
    _verify_webhook_signature=Depends(verify_webhook_signature),
    event_type=Depends(get_saleor_event),
):
    print(event_type)  # Use in case you have one handler for many event types
    print(await request.body())
    return "OK"


@app.post("/user_login", name="user_login")
async def user_login(saleor_user=Depends(get_saleor_user)):
    print(saleor_user)
    return "OK"

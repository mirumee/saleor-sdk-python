import abc
import logging

LOGGER = logging.getLogger(__name__)


class AbstractSaleorClient(abc.ABC):
    @abc.abstractmethod
    async def get_app_id(self, auth_token: str) -> str | None:
        """Call Saleor with the app token to see if it has access
        to it's own Saleor app record in Saleor"""

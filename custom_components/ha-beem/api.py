"""API client for Beem Energy."""
from datetime import date
import logging

import aiohttp
import async_timeout

from homeassistant import exceptions

from .const import API_BASE_URI, API_LOGIN

_LOGGER = logging.getLogger(__name__)


class BeemApiClient:
    """API client for Beem Energy."""

    def __init__(self, username: str, password: str, session: aiohttp.ClientSession, access_token: str | None = None) -> None:
        """Initialize API client."""
        self.username = username
        self.password = password
        self.session = session
        self.access_token = access_token

    async def authenticate(self) -> bool:
        """Test if we can authenticate with the host."""
        try:
            async with async_timeout.timeout(10):
                login_data = {"username": self.username, "password": self.password}
                async with self.session.post(
                    f"{API_BASE_URI}{API_LOGIN}", json=login_data
                ) as resp:
                    if resp.status == 404:
                        return False
                    resp.raise_for_status()
                    result = await resp.json()
                    self.access_token = result["token"]
                    return True
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error authenticating with Beem API: %s", err)
            return False

    async def get_box_summary(self, month: int, year: int) -> dict:
        """Get box summary."""
        try:
            async with async_timeout.timeout(10):
                headers = {"Authorization": f"Bearer {self.access_token}"}
                current_date = date(year, month, 1)
                async with self.session.get(
                    f"{API_BASE_URI}/box/summary/{current_date}",
                    headers=headers,
                ) as resp:
                    resp.raise_for_status()
                    return await resp.json()
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error getting box summary from Beem API: %s", err)
            return {}
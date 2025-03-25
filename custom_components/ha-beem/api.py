"""API client for Beem Energy."""
import asyncio
import logging
from datetime import date
import aiohttp
import async_timeout

from homeassistant import exceptions
from .const import API_BASE_URI, API_LOGIN, API_BOX

_LOGGER = logging.getLogger(__name__)


class BeemApiClient:
    """API client for Beem Energy."""

    def __init__(self, username: str, password: str, session: aiohttp.ClientSession, access_token: str | None = None) -> None:
        """Initialize API client."""
        self.email = username
        self.password = password
        self.session = session
        self.access_token = access_token

    async def authenticate(self) -> bool:
        """Authenticate and store the access token."""
        if self.access_token:
            return True  # Use existing token if available

        try:
            async with async_timeout.timeout(10):
                login_data = {"email": self.email, "password": self.password}
                async with self.session.post(
                    f"{API_BASE_URI}/{API_LOGIN}", json=login_data
                ) as resp:
                    if resp.status != 200:
                        _LOGGER.error(f"Authentication failed with status {resp.status}")
                        return False
                    result = await resp.json()
                    if "accessToken" not in result:
                        _LOGGER.error("No accessToken found in response")
                        return False
                    self.access_token = result["accessToken"]
                    _LOGGER.info("Successfully authenticated with Beem API")
                    return True
        except asyncio.TimeoutError as err:
            _LOGGER.error("Timeout while authenticating with Beem API: %s", err)
            return False
        except aiohttp.ClientError as err:
            _LOGGER.error("Client error while authenticating with Beem API: %s", err)
            return False
        except Exception as err:
            _LOGGER.error("Unexpected error while authenticating with Beem API: %s", err)
            return False

    async def get_box_summary(self, month: int, year: int) -> dict:
        """Fetch production summary data for a given month and year."""
        if not await self.authenticate():
            _LOGGER.error("Authentication failed. Cannot fetch box summary.")
            return {}

        try:
            async with async_timeout.timeout(10):
                headers = {"Authorization": f"{self.access_token}", "Content-Type": "application/json"}
                payload = {"month": month, "year": year}
                async with self.session.post(
                    f"{API_BASE_URI}/{API_BOX}",
                    headers=headers,
                    json=payload,
                ) as resp:
                    if resp.status not in (200,201):
                        _LOGGER.error(f"Failed to fetch box summary. Status: {resp.status}")
                        return {}
                    data = await resp.json()
                    if isinstance(data, list) and data:
                        return data[0]
                    return {}
        except asyncio.TimeoutError as err:
            _LOGGER.error("Timeout while fetching box summary: %s", err)
            return {}
        except aiohttp.ClientError as err:
            _LOGGER.error("Client error while fetching box summary: %s", err)
            return {}
        except Exception as err:
            _LOGGER.error("Unexpected error while fetching box summary from Beem API: %s", err)
            return {}

    async def get_current_production(self) -> dict:
        """Fetch current production data."""
        today = date.today()
        return await self.get_box_summary(today.month, today.year)

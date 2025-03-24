import asyncio
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import Throttle

from .api import BeemApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)  # Update interval for fetching data

class BeemUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Beem API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: BeemApiClient,
        config_entry,
    ):

        """Initialize the coordinator."""
        self.api = api
        self.config_entry = config_entry
        self.historical_months = 12  # Always fetch 12 months
        self._data = None
        self._historical_data = None
        self._last_updated = None

        # Initialize the DataUpdateCoordinator
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from the Beem API."""
        try:
            # Get current data
            current_data = await self.api.get_current_data()
            historical_data = None

            # If historical data is enabled, fetch it
            if self.historical_months > 0:
                historical_data = await self.api.get_historical_data(self.historical_months)

            # Store the fetched data
            self._data = current_data
            self._historical_data = historical_data

            # Update the last fetched time
            self._last_updated = asyncio.get_event_loop().time()

            return {
                "current": self._data,
                "historical": self._historical_data,
            }
        except Exception as err:
            raise UpdateFailed(f"Error fetching data from Beem API: {err}")

    async def fetch_data(self, month: int, year: int):
        """Fetch specific historical data based on the provided month and year."""
        try:
            return await self.api.get_historical_data_for_month(year, month)
        except Exception as err:
            _LOGGER.error("Error fetching historical data: %s", err)
            return None

    @property
    def data(self):
        """Return the latest data."""
        return self._data

    @property
    def historical_data(self):
        """Return the historical data."""
        return self._historical_data

    @property
    def last_updated(self):
        """Return the last time the data was updated."""
        return self._last_updated

    async def async_config_entry_first_refresh(self):
        """Perform the initial data refresh."""
        await self.async_refresh()

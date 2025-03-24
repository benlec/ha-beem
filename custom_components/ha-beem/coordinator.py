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
        self._data = None  # Store fetched data here
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
            current_data = await self.api.get_box_summary()

            # Store the fetched data in _data
            self._data = current_data

            # Update the last fetched time
            self._last_updated = asyncio.get_event_loop().time()

            # Return the fetched data, which will be managed by DataUpdateCoordinator
            return {
                "current": self._data,
            }

        except Exception as err:
            raise UpdateFailed(f"Error fetching data from Beem API: {err}")

    @property
    def data(self):
        """Return the latest data."""
        return self._data

    @property
    def last_updated(self):
        """Return the last time the data was updated."""
        return self._last_updated

    async def async_config_entry_first_refresh(self):
        """Perform the initial data refresh."""
        await self.async_refresh()

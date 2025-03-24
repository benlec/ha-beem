import asyncio
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import BeemApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)  # Update interval for fetching data

class BeemUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Beem API."""

    def __init__(self, hass: HomeAssistant, api: BeemApiClient, config_entry):
        """Initialize the coordinator."""
        self.api = api
        self.config_entry = config_entry

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from the Beem API."""
        try:
            current_data = await self.api.get_current_production()

            # Instead of assigning to self.data, use async_set_updated_data
            self.async_set_updated_data(current_data)

            return current_data

        except Exception as err:
            raise UpdateFailed(f"Error fetching data from Beem API: {err}")

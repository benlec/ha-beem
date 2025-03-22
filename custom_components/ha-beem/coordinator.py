"""DataUpdateCoordinator for the Beem Solar integration."""
from datetime import datetime, timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class BeemUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Beem data."""

    def __init__(self, hass: HomeAssistant, api) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )
        self.api = api
        self.platforms = []

    async def _async_update_data(self):
        """Update data via library."""
        now = dt.now()
        try:
            return await self.api.get_box_summary(now.month, now.year)
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.error("Error updating Beem data: %s", error)
            return None
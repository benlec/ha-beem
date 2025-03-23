"""DataUpdateCoordinator for the Beem Energy integration."""
import asyncio
import logging
from datetime import datetime, timedelta
import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.util import dt

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class BeemUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Beem data."""

    def __init__(self, hass: HomeAssistant, api, config_entry) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )
        self.api = api
        self.historical_months = config_entry.data.get(CONF_FETCH_HISTORICAL, 0)
        self.platforms = []

    async def _async_update_data(self):
        """Update data via library."""
        data = {}
        now = dt.now()
        
        # Always fetch current month
        current_month_data = await self.fetch_data(now.month, now.year)
        if current_month_data:
            data[f"{now.year}-{now.month:02d}"] = current_month_data

        # Fetch historical data if configured
        for i in range(1, self.historical_months + 1):
            historical_date = now - timedelta(days=i*30)  # Approximate month calculation
            month_data = await self.fetch_data(historical_date.month, historical_date.year)
            if month_data:
                data[f"{historical_date.year}-{historical_date.month:02d}"] = month_data

        return data

    async def fetch_data(self, month: int, year: int) -> dict | None:
        """Fetch data for a specific month and year."""
        try:
            return await self.api.get_box_summary(month, year)
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error fetching data for %d-%02d: %s", year, month, err)
            return None
        except asyncio.TimeoutError as error:
            _LOGGER.error("Timeout while updating Beem data: %s", error)
            return None
        except aiohttp.ClientError as error:
            _LOGGER.error("Client error while updating Beem data: %s", error)
            return None
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.error("Unexpected error while updating Beem data: %s", error)
            return None
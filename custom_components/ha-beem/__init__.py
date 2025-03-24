"""The Beem Energy Integration."""
import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import aiohttp_client

from .api import BeemApiClient
from .coordinator import BeemUpdateCoordinator
from .helpers import load_token_from_secrets
from .const import DOMAIN

SCAN_INTERVAL = timedelta(minutes=1)
PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Beem Energy component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Beem Energy from a config entry."""
    session = aiohttp_client.async_get_clientsession(hass)
    
    # Fetch token from secrets
    access_token = await load_token_from_secrets(hass)

    api = BeemApiClient(
        username=entry.data["username"],
        password=entry.data["password"],
        session=session,
        access_token=access_token,
    )
    
    # Initialize the coordinator with a fixed 12-month historical fetch
    coordinator = BeemUpdateCoordinator(hass, api, entry, historical_months=12)
    await coordinator.async_config_entry_first_refresh()
    
    # Store the coordinator instance
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    async def fetch_historical_data(call: ServiceCall) -> None:
        """Handle fetching historical data."""
        month = call.data["month"]
        year = call.data["year"]
        entry_id = call.data.get("entry_id", entry.entry_id)  # Default to current entry
        coordinator = hass.data[DOMAIN].get(entry_id)
        
        if coordinator:
            data = await coordinator.fetch_data(month, year)
            if data:
                await coordinator.async_refresh()
        else:
            _LOGGER.warning("Coordinator not found for entry_id: %s", entry_id)
    
    hass.services.async_register(DOMAIN, "fetch_historical_data", fetch_historical_data)
    
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

        # If no more entries exist, remove DOMAIN from hass.data
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)

    return unload_ok

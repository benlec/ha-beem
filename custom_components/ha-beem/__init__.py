"""The Beem Solar Integration."""
import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import aiohttp_client

from .api import BeemApiClient
from .coordinator import BeemUpdateCoordinator
from .const import DOMAIN

SCAN_INTERVAL = timedelta(minutes=1)
PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Beem Solar component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Beem Solar from a config entry."""
    session = aiohttp_client.async_get_clientsession(hass)
    
    api = BeemApiClient(
        username=entry.data["username"],
        password=entry.data["password"],
        session=session,
    )
    
    coordinator = BeemUpdateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    async def fetch_historical_data(call: ServiceCall) -> None:
        """Handle fetching historical data."""
        month = call.data["month"]
        year = call.data["year"]
        coordinator = next(iter(hass.data[DOMAIN].values()))
        data = await coordinator.fetch_data(month, year)
        if data:
            await coordinator.async_refresh()
    
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
        hass.data["ha-beem"].pop(entry.entry_id)

    return unload_ok
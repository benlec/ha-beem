"""The Beem Energy Integration."""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client

from .helpers import load_token_from_secrets
from .api import BeemApiClient
from .coordinator import BeemUpdateCoordinator
from .const import DOMAIN

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Beem Energy component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Beem Energy from a config entry."""
    session = aiohttp_client.async_get_clientsession(hass)

    # Retrieve access token (this function should exist in helpers.py)
    access_token = await load_token_from_secrets(hass)
    _LOGGER.debug("Loaded access token: %s", access_token)
    
    api = BeemApiClient(
        username=entry.data["username"],
        password=entry.data["password"],
        session=session,
        access_token=access_token
    )
    
    coordinator = BeemUpdateCoordinator(hass, api, entry)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
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
        
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)
    
    return unload_ok

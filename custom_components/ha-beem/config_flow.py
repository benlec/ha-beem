"""Config flow for Beem Energy integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from .const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import BeemApiClient
from .helpers import load_token_from_secrets, save_token_to_secrets

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME, default=""): str,
        vol.Required(CONF_PASSWORD, default=""): str,
    } 
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""

    session = async_get_clientsession(hass)
    client = BeemApiClient(
        data[CONF_USERNAME],
        data[CONF_PASSWORD],
        session,
        await load_token_from_secrets(hass),  # Pass token from secrets
    )

    try:
        if not await client.authenticate():  # This will also get and set the token if successful
            _LOGGER.error("Invalid authentication for email: %s", data[CONF_USERNAME])
            raise InvalidAuth
    except Exception as err:
        _LOGGER.error("Error connecting to Beem API: %s", err)
        raise CannotConnect

    # Now that authentication is successful, the token should be available
    token = client.access_token
    if token:
        await save_token_to_secrets(hass, token)  # Save the token to secrets.yaml

    # Returning the data for creating the config entry

    return {
        "title": data[CONF_USERNAME]     
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Beem Energy."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await self.async_set_unique_id(user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured()
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

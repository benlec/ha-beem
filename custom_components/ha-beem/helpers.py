"""Helper functions for the Beem Solar integration."""
import json
import logging
from pathlib import Path

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


def load_token_from_secrets(hass: HomeAssistant) -> str | None:
    """Load access token from secrets file."""
    try:
        secrets_file = Path(hass.config.path("secrets.yaml"))
        with open(secrets_file, encoding="utf8") as file:
            secrets = json.loads(file.read())
            return secrets.get("beem_token")
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.error("Error loading token from secrets: %s", err)
        return None


def save_token_to_secrets(hass: HomeAssistant, token: str) -> None:
    """Save access token to secrets file."""
    try:
        secrets_file = Path(hass.config.path("secrets.yaml"))
        with open(secrets_file, "r", encoding="utf8") as file:
            secrets = json.loads(file.read())

        secrets["beem_token"] = token

        with open(secrets_file, "w", encoding="utf8") as file:
            json.dump(secrets, file, indent=4)
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.error("Error saving token to secrets: %s", err)
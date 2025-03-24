"""Helper functions for the Beem Solar integration."""
import yaml
import asyncio
import logging
from pathlib import Path
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

async def load_token_from_secrets(hass: HomeAssistant) -> str | None:
    """Load access token from secrets.yaml file (YAML format) asynchronously."""
    try:
        secrets_file = Path(hass.config.path("secrets.yaml"))

        # Run file operations in a separate thread to avoid blocking
        def read_from_file():
            if not secrets_file.exists():
                _LOGGER.info("secrets.yaml not found. Returning None.")
                return None

            with open(secrets_file, encoding="utf8") as file:
                secrets = yaml.safe_load(file) or {}

            if "beem_token" not in secrets:
                _LOGGER.info("Token not found in secrets.yaml.")
                return None

            return secrets["beem_token"]

        return await asyncio.to_thread(read_from_file)

    except yaml.YAMLError:
        _LOGGER.error("Malformed secrets.yaml file.")
        return None
    except Exception as err:
        _LOGGER.error("Error loading token from secrets: %s", err)
        return None


async def save_token_to_secrets(hass: HomeAssistant, token: str) -> None:
    """Save access token to secrets.yaml file (YAML format) asynchronously."""
    try:
        secrets_file = Path(hass.config.path("secrets.yaml"))

        # Run file operations in a separate thread to avoid blocking
        def write_to_file():
            if not secrets_file.exists():
                _LOGGER.info("secrets.yaml not found. Creating the file...")
                secrets_file.touch()

            secrets = {}
            if secrets_file.stat().st_size > 0:
                with open(secrets_file, "r", encoding="utf8") as file:
                    secrets = yaml.safe_load(file) or {}

            secrets["beem_token"] = token

            with open(secrets_file, "w", encoding="utf8") as file:
                yaml.dump(secrets, file, default_flow_style=False, allow_unicode=True)

            _LOGGER.info("Token saved to secrets.yaml.")

        await asyncio.to_thread(write_to_file)

    except Exception as err:
        _LOGGER.error("Error saving token to secrets: %s", err)

"""Support for Beem Solar sensors."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import BeemUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Beem Solar sensors."""
    coordinator: BeemUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        BeemMonthlyEnergySensor(coordinator),
        BeemDailyEnergySensor(coordinator),
        BeemPowerSensor(coordinator),
    ]

    async_add_entities(entities)


class BeemBaseSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Beem sensor."""

    _attr_has_entity_name = True

    @property
    def device_info(self):
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, "solar")},
            name="Beem Solar",
            manufacturer="Beem Energy",
            model="Beem Kit",
        )


class BeemMonthlyEnergySensor(BeemBaseSensor):
    """Representation of a Beem monthly energy sensor."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator: BeemUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "monthly_energy"
        self._attr_name = "Monthly Energy"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("monthlyEnergy", 0) / 1000


class BeemDailyEnergySensor(BeemBaseSensor):
    """Representation of a Beem daily energy sensor."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator: BeemUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "daily_energy"
        self._attr_name = "Daily Energy"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("dailyEnergy", 0) / 1000


class BeemPowerSensor(BeemBaseSensor):
    """Representation of a Beem power sensor."""

    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.WATT

    def __init__(self, coordinator: BeemUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "current_power"
        self._attr_name = "Current Power"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        try:
            power_value = self.coordinator.data.get("currentPower", 0)
            return round(float(power_value), 2)
        except (TypeError, ValueError):
            _LOGGER.error("Invalid power value received from Beem API")
            return None
            return None
        return self.coordinator.data.get("power", 0)
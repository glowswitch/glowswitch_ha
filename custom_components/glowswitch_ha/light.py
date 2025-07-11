"""Light platform for GlowSwitch HA."""
from __future__ import annotations

import logging
from typing import Any

from bleak_retry_connector import BleakClientWithServiceCache, establish_connection

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components import bluetooth

from .const import DOMAIN, GLOWSWITCH_SERVICE_UUID, GLOWDIM_SERVICE_UUID, LIGHT_CHARACTERISTIC_UUID

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the GlowSwitch light platform."""
    address = entry.unique_id
    ble_device = bluetooth.async_ble_device_from_address(hass, address)
    if not ble_device:
        _LOGGER.warning("GlowSwitch device not found at address %s", address)
        return

    service_info = bluetooth.async_last_service_info(hass, address)
    is_dimmable = GLOWDIM_SERVICE_UUID in service_info.service_uuids

    light = GlowDim(ble_device) if is_dimmable else GlowSwitch(ble_device)
    async_add_entities([light])


class GlowLight(LightEntity):
    """Base class for GlowSwitch lights."""

    _attr_assumed_state = True
    _attr_has_entity_name = True

    def __init__(self, ble_device) -> None:
        """Initialize the light."""
        self._ble_device = ble_device
        self._client: BleakClientWithServiceCache | None = None
        self._attr_unique_id = ble_device.address
        self._attr_device_info = DeviceInfo(
            connections={("bluetooth", ble_device.address)},
            name=ble_device.name,
            manufacturer="GlowSwitch",
        )

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        self._client = await establish_connection(
            BleakClientWithServiceCache,
            self._ble_device,
            self.unique_id,
        )

    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        if self._client:
            await self._client.disconnect()
        await super().async_will_remove_from_hass()

    async def _send_data(self, data: bytearray) -> None:
        """Send data to the light."""
        if not self._client:
            _LOGGER.debug("No client available")
            return
        try:
            await self._client.write_gatt_char(LIGHT_CHARACTERISTIC_UUID, data, response=True)
        except Exception as e:
            _LOGGER.error("Error sending data: %s", e)


class GlowSwitch(GlowLight):
    """Representation of a GlowSwitch on/off light."""

    def __init__(self, ble_device) -> None:
        """Initialize the GlowSwitch."""
        super().__init__(ble_device)
        self._attr_name = "Switch"
        self._attr_supported_color_modes = {ColorMode.ONOFF}
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        await self._send_data(bytearray([0x01]))
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        await self._send_data(bytearray([0x00]))
        self._attr_is_on = False
        self.async_write_ha_state()


class GlowDim(GlowLight):
    """Representation of a GlowSwitch dimmable light."""

    def __init__(self, ble_device) -> None:
        """Initialize the GlowDim."""
        super().__init__(ble_device)
        self._attr_name = "Dimmable Light"
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        self._attr_supported_features = LightEntityFeature.TRANSITION
        self._attr_is_on = False
        self._attr_brightness = 0

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        brightness = kwargs.get(ATTR_BRIGHTNESS, self.brightness or 255)
        # Scale brightness from 0-255 to 0-100
        scaled_brightness = int((brightness / 255) * 100)
        
        await self._send_data(bytearray([scaled_brightness]))
        self._attr_is_on = True
        self._attr_brightness = brightness
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        await self._send_data(bytearray([0x00]))
        self._attr_is_on = False
        self._attr_brightness = 0
        self.async_write_ha_state()

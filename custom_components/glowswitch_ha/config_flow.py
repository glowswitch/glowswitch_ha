"""Config flow for GlowSwitch HA."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, GLOWSWITCH_SERVICE_UUID, GLOWDIM_SERVICE_UUID

_LOGGER = logging.getLogger(__name__)


class GlowSwitchConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for GlowSwitch HA."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle the bluetooth discovery step."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()

        self._discovery_info = discovery_info
        self.context["title_placeholders"] = {"name": discovery_info.name}
        return await self.async_step_confirm()

    async def async_step_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery."""
        if user_input is not None:
            return self.async_create_entry(
                title=self._discovery_info.name, data={}
            )

        self._set_confirm_only()
        return self.async_show_form(
            step_id="confirm",
            description_placeholders={"name": self._discovery_info.name},
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the user step to pick a device."""
        if user_input is not None:
            # Handle user-initiated setup if needed, for now we focus on discovery
            return self.async_abort(reason="not_supported")

        current_addresses = self._async_current_ids()
        for discovery_info in async_discovered_service_info(self.hass):
            if discovery_info.address in current_addresses:
                continue

            if GLOWSWITCH_SERVICE_UUID in discovery_info.service_uuids or GLOWDIM_SERVICE_UUID in discovery_info.service_uuids:
                return await self.async_step_bluetooth(discovery_info)

        return self.async_abort(reason="no_devices_found")

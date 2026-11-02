"""Virtual TV media player entity."""
from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_NAME, CONF_POWER_ON_BUTTON, CONF_POWER_OFF_BUTTON


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Virtual TV entity."""
    config = {**entry.data, **entry.options}
    async_add_entities([VirtualTV(hass, entry, config)])


class VirtualTV(MediaPlayerEntity):
    """A virtual TV forwarding ON/OFF to separate input_button entities."""

    _attr_has_entity_name = True
    _attr_device_class = MediaPlayerDeviceClass.TV
    _attr_icon = "mdi:television"
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON | MediaPlayerEntityFeature.TURN_OFF
    )
    _attr_assumed_state = True
    # Keep the HA entity available at all times. Yandex's state_unknown option
    # hides/ignores this placeholder state and displays separate ON/OFF actions.
    _attr_state = MediaPlayerState.IDLE

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, config: dict) -> None:
        """Initialize the virtual TV."""
        self.hass = hass
        self._power_on_button = config[CONF_POWER_ON_BUTTON]
        self._power_off_button = config[CONF_POWER_OFF_BUTTON]
        self._attr_name = config.get(CONF_NAME, "Телевизор")
        self._attr_unique_id = entry.unique_id or "virtual_tv"

    async def async_turn_on(self) -> None:
        """Press the configured POWER ON input button."""
        await self.hass.services.async_call(
            "input_button",
            "press",
            {"entity_id": self._power_on_button},
            blocking=True,
        )

    async def async_turn_off(self) -> None:
        """Press the configured POWER OFF input button."""
        await self.hass.services.async_call(
            "input_button",
            "press",
            {"entity_id": self._power_off_button},
            blocking=True,
        )

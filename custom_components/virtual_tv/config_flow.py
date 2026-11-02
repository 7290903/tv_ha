"""Config flow for Virtual TV."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_NAME,
    CONF_POWER_ON_BUTTON,
    CONF_POWER_OFF_BUTTON,
)


class VirtualTVConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Virtual TV."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Set up Virtual TV."""
        errors = {}

        if user_input is not None:
            if user_input[CONF_POWER_ON_BUTTON] == user_input[CONF_POWER_OFF_BUTTON]:
                errors["base"] = "buttons_must_be_different"
            else:
                await self.async_set_unique_id("virtual_tv")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Телевизор"): str,
                vol.Required(CONF_POWER_ON_BUTTON): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="input_button")
                ),
                vol.Required(CONF_POWER_OFF_BUTTON): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="input_button")
                ),
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return options flow."""
        return VirtualTVOptionsFlow(config_entry)


class VirtualTVOptionsFlow(config_entries.OptionsFlow):
    """Options flow for Virtual TV."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = {**self.config_entry.data, **self.config_entry.options}
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_NAME, default=current.get(CONF_NAME, "Телевизор")
                ): str,
                vol.Required(
                    CONF_POWER_ON_BUTTON,
                    default=current[CONF_POWER_ON_BUTTON],
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="input_button")
                ),
                vol.Required(
                    CONF_POWER_OFF_BUTTON,
                    default=current[CONF_POWER_OFF_BUTTON],
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="input_button")
                ),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)

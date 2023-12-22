"""Siren platform for dahua."""
from homeassistant.core import HomeAssistant
from homeassistant.components.siren import SirenEntity
from custom_components.dahua import DahuaDataUpdateCoordinator

from .const import DOMAIN, SIREN_ICON
from .entity import DahuaBaseEntity
from .client import SIREN_TYPE


async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator: DahuaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    devices = []

    # Only some cams have a siren, very few do actually
    if coordinator.supports_siren():
        devices.append(DahuaSiren(coordinator, entry))

    async_add_devices(devices)


class DahuaSiren(DahuaBaseEntity, SirenEntity):
    """dahua siren siren class. Used to enable or disable camera built in sirens"""

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on/enable the camera's siren"""
        channel = self._coordinator.get_channel()
        await self._coordinator.client.async_set_coaxial_control_state(channel, SIREN_TYPE, True)
        await self._coordinator.async_refresh()

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off/disable camera siren"""
        channel = self._coordinator.get_channel()
        await self._coordinator.client.async_set_coaxial_control_state(channel, SIREN_TYPE, False)
        await self._coordinator.async_refresh()

    @property
    def name(self):
        """Return the name of the siren."""
        return self._coordinator.get_device_name() + " Siren"

    @property
    def unique_id(self):
        """
        A unique identifier for this entity. Needs to be unique within a platform (ie light.hue). Should not be configurable by the user or be changeable
        see https://developers.home-assistant.io/docs/entity_registry_index/#unique-id-requirements
        """
        return self._coordinator.get_serial_number() + "_siren"

    @property
    def icon(self):
        """Return the icon of this siren."""
        return SIREN_ICON

    @property
    def available_tones(self):
        """Return the tones available for the siren."""
        tones = [
            "alarm",
        ]
        return tones

    @property
    def is_on(self):
        """
        Return true if the siren is on.
        Value is fetched from api.get_motion_detection_config
        """
        return self._coordinator.is_siren_on()

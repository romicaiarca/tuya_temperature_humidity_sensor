"""Platform for sensor integration."""
from __future__ import annotations

import voluptuous as vol
import json
import array as arr
import logging
from .TemperatureHumiditySensor import TemperatureHumiditySensor

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    TEMP_CELSIUS,
    PERCENTAGE,
    CONF_REGION,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

devices = []

ENTITIES_SCHEMA = vol.Schema({
    vol.Required("device_id", default=""): cv.string,
})

SENSORS_SCHEMA = vol.All({
    vol.Required("category", default="wsdcg"): "wsdcg",
    vol.Required("entities", default=[]): vol.All(cv.ensure_list, [ENTITIES_SCHEMA]),
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_REGION, default=""): cv.string,
    vol.Required(CONF_CLIENT_ID, default=""): cv.string,
    vol.Required(CONF_CLIENT_SECRET, default=""): cv.string,
    vol.Required("sensors", default={}): SENSORS_SCHEMA,
})

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""

    sensors = config.get("sensors")
    sensorsEntities = sensors["entities"]

    entities = []

    for deviceEntry in sensorsEntities:
        for key, device in deviceEntry.items():
            entities.append(TemperatureHumiditySensor(device, 'temperature', config, hass))
            entities.append(TemperatureHumiditySensor(device, 'humidity', config, hass))
            entities.append(TemperatureHumiditySensor(device, 'battery_percentage', config, hass))

    async_add_entities(entities)



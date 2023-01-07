import tinytuya

from homeassistant.const import (
    TEMP_CELSIUS,
    PERCENTAGE,
    CONF_REGION,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass
)

class TemperatureHumiditySensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, device, measurement_type, config) -> None:
        """Initialize the DHT sensor"""

        self.config = config
        self.measurement_type = measurement_type
        self.device = device
        self._attr_name = f"Temperature DHT ({measurement_type=})"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_value = 0


        if measurement_type == 'temperature':
            self._attr_native_unit_of_measurement = TEMP_CELSIUS
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
        elif measurement_type == 'battery_percentage':
            self._attr_device_class = SensorDeviceClass.BATTERY

        self.update()

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        dataFromTuya = self.getDataFromTuya()

        if "device_name" not in dataFromTuya.keys() or "va_temperature" not in dataFromTuya.keys() or "va_humidity" not in dataFromTuya.keys() or "battery_percentage" not in dataFromTuya.keys():
            _LOGGER.error(f"Missing data for the device {self.device=}.")
            return None

        self._attr_name = dataFromTuya["device_name"] + "_" + self.measurement_type

        if self.measurement_type == 'temperature':
            self._attr_native_value = dataFromTuya["va_temperature"]
        elif self.measurement_type == 'battery_percentage':
            self._attr_native_value = dataFromTuya["battery_percentage"]
        else:
            self._attr_native_value = dataFromTuya["va_humidity"]

    def getDataFromTuya(self):
        apiRegion = self.config.get(CONF_REGION)
        apiKey = self.config.get(CONF_CLIENT_ID)
        apiSecret = self.config.get(CONF_CLIENT_SECRET)
        apiDeviceID = self.device

        # tinytuya.set_debug(True, False)

        dht = tinytuya.Cloud(
            self.config.get(CONF_REGION),
            self.config.get(CONF_CLIENT_ID),
            self.config.get(CONF_CLIENT_SECRET),
            apiDeviceID
        )

        device_name = 'Unknown'
        devices = dht.getdevices()
        category = self.config.get("sensors")['category']

        for device in devices:
            if device["id"] == apiDeviceID:
                if device["category"] != category:
                    _LOGGER.error(f"Unsupported device {apiDeviceID=}.")
                    return {}
                
                device_name = device["name"]

        dhtProperties = dht.getproperties(apiDeviceID)

        if dhtProperties is None:
            _LOGGER.error(f"No properties for the device: {apiDeviceID=}.")
        #     # print(f"No properties for the device: {apiDeviceID=}.")
            return 1

        if dhtProperties['success'] is not True:
            _LOGGER.error(f"We encounter isssues getting properties with success for the device: {apiDeviceID=}.")
            # print(f"We encounter isssues getting properties with success for the device: {apiDeviceID=}.")
            return 2


        if dhtProperties['result'] is None and dhtProperties['result']['category'] is None:
            _LOGGER.error(f"We couldn't get the category for the device: {apiDeviceID=}.")
            # print(f"We couldn't get the category for the device: {apiDeviceID=}.")
            return 3

        if dhtProperties['result']['category'] != "wsdcg":
            _LOGGER.error(f"The device: {apiDeviceID=} is not a DHT sensor.")
            # print(f"The device: {apiDeviceID=} is not a DHT sensor.")
            return 4


        if dhtProperties['result']['status'] is None:
            _LOGGER.error(f"We can't get the status for the device: {apiDeviceID=}.")
            # print(f"We can't get the status for the device: {apiDeviceID=}.")
            return 5

        dhtStatus = dht.getstatus(apiDeviceID)

        if dhtStatus['success'] is not True:
            _LOGGER.error(f"We encounter isssues getting status with success for the device: {apiDeviceID=}.")
            # print(f"We encounter isssues getting status with success for the device: {apiDeviceID=}.")
            return 6

        if dhtStatus['result'] is None:
            _LOGGER.error(f"We can't get the status for the device: {apiDeviceID=}.")
            # print(f"We can't get the status for the device: {apiDeviceID=}.")
            return 7

        statuses = dhtStatus['result']

        response = {}
        response["va_temperature"] = dhtStatus['result'][0]["value"] / 10
        response["va_humidity"] = dhtStatus['result'][1]["value"] / 10
        response["battery_percentage"] = dhtStatus['result'][2]["value"]
        response["device_name"] = device_name

        return response

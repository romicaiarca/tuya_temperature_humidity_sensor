# Tuya Temperature Humidity Sensor

This is a minimum implementation of an integration providing a sensor measurement (Temperature and Humidity) from Tuya Cloud using TinyTuya.
Thes was implemented since for the moment Tuya integration doesn't support such sensors,
I am still working to implement same think in TinyTuya for local, to avoid connections and requests to Tuya Cloud.

### Installation

Copy this folder to `<config_dir>/custom_components/tuya_temperature_humidity_sensor/`.

Add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
sensor:
  - platform: tuya_temperature_humidity_sensor
    region: "eu"
    client_id: "frtc...fuo1"
    client_secret: "2481...a80e"
    sensors:
      category: "wsdcg"
      entities:
        - device_id: "bf26...m2gu" # device_id
        - device_id: "bf24...n8xt" # device_id
        - device_id: "bf25...ygxv" # device_id
```
Author: Romică Iarca [@romicaiarca](https://github.com/romicaiarca)

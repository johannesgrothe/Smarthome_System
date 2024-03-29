"""Collection of constants for all gadgets"""

# This file was generated by 'constants_exporter_gadgets_python.py' at 'https://github.com/johannesgrothe/Smarthome_System'
# Do not modify this file, modify 'api_docs/api_specs.json' and 'gadget_docs/gadget_specs.json' and export.
# Every change made will be overwritten at next export.

import enum


class RemoteGadgetIdentifier(enum.IntEnum):
    """Gadgets running on the ESP clients (remote gadgets)"""

    lamp_neopixel_rgb_basic = 0  # NeoPixel Basic RGB Lamp
    lamp_basic = 1  # Basic Lamp
    fan_westinghouse_ir = 2  # Westinghouse IR Fan
    lamp_westinghouse_ir = 3  # Westinghouse IR Fan Lamp
    doorbell_basic = 4  # Doorbell Basic
    wallswitch_basic = 5  # Basic Wallswitch
    sensor_motion_hr501 = 6  # HR501 Motion Sensor
    sensor_temperature_dht = 7  # DHT Temperature/Humidity Sensor


class LocalGadgetIdentifier(enum.IntEnum):
    """Gadgets running on the bridge itself (local gadget)"""

    denon_av_receiver = 0  # Denon AV Receiver


class GadgetClass(enum.IntEnum):
    """General categories of gadgets. Two gadgets of the same class have the same attributes but may differ in implemetation"""

    lamp = 0  # Lamp
    lamp_adjustable = 1  # Adjustable Lamp
    lamp_rgb = 2  # RGB Lamp
    fan = 3  # Fan
    tv = 4  # TV
    media_player = 5  # Media Player
    hum_sensor = 6  # Humidity Sensor
    temp_sensor = 7  # Temperature Sensor
    hum_temp_sensor = 8  # Humidity + Temperature Sensor
    mov_sensor = 9  # Movement Sensor
    doorbell = 10  # Doorbell
    stateless_switch = 11  # Stateless Switch
    state_switch = 12  # Switch


GadgetClassMapping = {
    GadgetClass.lamp: [RemoteGadgetIdentifier.lamp_basic, RemoteGadgetIdentifier.lamp_westinghouse_ir],
    GadgetClass.lamp_adjustable: [],
    GadgetClass.lamp_rgb: [RemoteGadgetIdentifier.lamp_neopixel_rgb_basic],
    GadgetClass.fan: [RemoteGadgetIdentifier.fan_westinghouse_ir],
    GadgetClass.tv: [LocalGadgetIdentifier.denon_av_receiver],
    GadgetClass.media_player: [],
    GadgetClass.hum_sensor: [],
    GadgetClass.temp_sensor: [],
    GadgetClass.hum_temp_sensor: [RemoteGadgetIdentifier.sensor_temperature_dht],
    GadgetClass.mov_sensor: [RemoteGadgetIdentifier.sensor_motion_hr501],
    GadgetClass.doorbell: [RemoteGadgetIdentifier.doorbell_basic],
    GadgetClass.stateless_switch: [RemoteGadgetIdentifier.wallswitch_basic],
    GadgetClass.state_switch: []
}

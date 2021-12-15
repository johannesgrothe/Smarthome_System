"""Collection of constants for all gadgets and characteristics"""

# This file was generated by 'gadget_constants_exporter.py' at 'https://github.com/johannesgrothe/Smarthome_System'
# Do not modify this file, modify 'gadget_docs/gadget_specs.json' and export.
# Every change made will be overwritten at next export.

try:
    from lib.system_identifier import SystemIdentifier
except ModuleNotFoundError:
    from .lib.system_identifier import SystemIdentifier


class CharacteristicIdentifier(SystemIdentifier):
    """Characteristics Gadgets can contain"""

    err_type = 0  # Error-Characteristic
    status = 1  # Status
    fan_speed = 2  # Fan Speed
    brightness = 3  # Brightness
    hue = 4  # Hue
    saturation = 5  # Saturation
    temperature = 6  # Temperature
    humidity = 7  # Humidity


class GadgetIdentifier(SystemIdentifier):
    """Gadgets running on the ESP Clients"""

    any_gadget = 0                  # Any Gadget
    lamp_neopixel_rgb_basic = 1     # NeoPixel Basic RGB Lamp
    lamp_basic = 2                  # Basic Lamp
    fan_westinghouse_ir = 3         # Westinghouse IR Fan
    lamp_westinghouse_ir = 4        # Westinghouse IR Fan Lamp
    doorbell_basic = 5              # Doorbell Basic
    wallswitch_basic = 6            # Basic Wallswitch
    sensor_motion_hr501 = 7         # HR501 Motion Sensor
    sensor_temperature_dht = 8      # DHT Temperature/Humidity Sensor


class BridgeGadgetIdentifier(SystemIdentifier):
    """Gadgets running on the Bridge itself (virtual Gadgets)"""


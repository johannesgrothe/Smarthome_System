#pragma once
// Collection of constants for all gadgets

// This file was generated by 'constants_exporter_gadgets_cpp.py' at 'https://github.com/johannesgrothe/Smarthome_System'
// Do not modify this file, modify 'api_docs/api_specs.json' and 'gadget_docs/gadget_specs.json' and export.
// Every change made will be overwritten at next export.

#include <cstdint>

// Namespace for all gadget and characteristic definitions
namespace gadget_definitions {

    // Count of the different gadget identifiers
    constexpr uint8_t GadgetIdentifierCount = 8;

    // Gadgets running on the ESP clients (remote gadgets)
    enum class GadgetIdentifier {
        lamp_neopixel_rgb_basic = 0,  // NeoPixel Basic RGB Lamp
        lamp_basic = 1,  // Basic Lamp
        fan_westinghouse_ir = 2,  // Westinghouse IR Fan
        lamp_westinghouse_ir = 3,  // Westinghouse IR Fan Lamp
        doorbell_basic = 4,  // Doorbell Basic
        wallswitch_basic = 5,  // Basic Wallswitch
        sensor_motion_hr501 = 6,  // HR501 Motion Sensor
        sensor_temperature_dht = 7  // DHT Temperature/Humidity Sensor
    };
}

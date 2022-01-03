
// CLass for all gadget and characteristic definitions
export default class GadgetDefinitions {

    // Count of the different gadget identifiers
    static GadgetIdentifierCount = 9;

    // Count of the different characteristic identifiers
    static CharacteristicIdentifierCount = 8;

    // Gadget Identifier
    static gadget_any_gadget = 0;  // Any Gadget
    static gadget_lamp_neopixel_rgb_basic = 1;  // NeoPixel Basic RGB Lamp
    static gadget_lamp_basic = 2;  // Basic Lamp
    static gadget_fan_westinghouse_ir = 3;  // Westinghouse IR Fan
    static gadget_lamp_westinghouse_ir = 4;  // Westinghouse IR Fan Lamp
    static gadget_doorbell_basic = 5;  // Doorbell Basic
    static gadget_wallswitch_basic = 6;  // Basic Wallswitch
    static gadget_sensor_motion_hr501 = 7;  // HR501 Motion Sensor
    static gadget_sensor_temperature_dht = 8;  // DHT Temperature/Humidity Sensor

    // Characteristic Identifier
    static characteristic_err_type = 0;  // Error-Characteristic
    static characteristic_status = 1;  // Status
    static characteristic_fan_speed = 2;  // Fan Speed
    static characteristic_brightness = 3;  // Brightness
    static characteristic_hue = 4;  // Hue
    static characteristic_saturation = 5;  // Saturation
    static characteristic_temperature = 6;  // Temperature
    static characteristic_humidity = 7;  // Humidity
}

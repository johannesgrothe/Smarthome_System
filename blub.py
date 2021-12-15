try:
    from lib.system_identifier import SystemIdentifier
except ModuleNotFoundError:
    from .lib.system_identifier import SystemIdentifier


class GadgetIdentifier(SystemIdentifier):
    any_gadget = 0
    lamp_neopixel_basic = 1
    lamp_basic = 2
    fan_westinghouse_ir = 3

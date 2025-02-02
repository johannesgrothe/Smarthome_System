import enum

class HwVariant(enum.IntEnum):
    """Hardware Variants"""
    unknown = 1  # Element representing any error case
    single_port = 2  # Simple controller setup with a single port exposed

class SwVariant(enum.IntEnum):
    """Software Variants"""
    unknown = 1  # Element representing any error case
    single_neopixel = 2  # Just single neopixel gadget

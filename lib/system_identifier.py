import enum


class SystemIdentifier(enum.IntEnum):

    @classmethod
    def get_attributes(cls):
        return [x for x in cls.__dict__.keys() if not x.startswith("_") and not callable(getattr(cls, x))]

    @classmethod
    def from_string(cls, value: str):
        if value not in cls.get_attributes():
            raise ValueError(value)
        return cls(getattr(cls, value))

    @classmethod
    def from_int(cls, value: int):
        return cls(value)

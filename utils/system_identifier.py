import enum


class SystemIdentifier:

    @classmethod
    def get_attributes(cls):
        return [x for x in cls.__dict__.keys() if not x.startswith("_") and not callable(getattr(cls, x))]

    @classmethod
    def from_string(cls, value: str):
        return cls(getattr(cls, value))

    def to_string(self) -> str:
        return self.__dict__["_name_"]


class IntSystemIdentifier(SystemIdentifier, enum.IntEnum):
    @classmethod
    def from_int(cls, value: int):
        return cls(value)

    def to_int(self) -> int:
        return int(self)


class StringSystemIdentifier(SystemIdentifier, enum.Enum):
    pass

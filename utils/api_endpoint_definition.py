import enum
from typing import Optional


class ApiAccessLevelSuper:
    pass


class ApiAccessType(enum.IntEnum):
    read = 0
    write = 1


class ApiEndpointDefinition:
    uri: str
    access_levels: list[ApiAccessLevelSuper]
    access_type: Optional[ApiAccessType]

    def __init__(self, uri: str, access_levels: list[ApiAccessLevelSuper], access_type: Optional[ApiAccessType]):
        self.uri = uri
        self.access_levels = access_levels
        self.access_type = access_type


class ApiURIsSuper:
    @classmethod
    def _get_endpoints(cls) -> list[ApiEndpointDefinition]:
        return [getattr(cls, x) for x in cls.__dict__.keys() if isinstance(getattr(cls, x), ApiEndpointDefinition)]

    @classmethod
    def get_definition_for_uri(cls, value: str):
        for endpoint in cls._get_endpoints():
            if endpoint.uri == value:
                return endpoint
        raise ValueError(value)

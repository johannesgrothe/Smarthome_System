import enum
from typing import Optional


class ApiAccessLevelSuper:
    pass


class ApiEndpointCategorySuper:
    pass


class ApiAccessType(enum.IntEnum):
    read = 0
    write = 1


class ApiEndpointDefinition:
    _uri: str
    _access_levels: list[ApiAccessLevelSuper]
    _category: Optional[ApiEndpointCategorySuper]
    _access_type: Optional[ApiAccessType]
    _outgoing: bool

    def __init__(self, uri: str, access_levels: list[ApiAccessLevelSuper], category: Optional[ApiEndpointCategorySuper],
                 access_type: Optional[ApiAccessType], outgoing: bool):
        self._uri = uri
        self._access_levels = access_levels
        self._category = category
        self._access_type = access_type
        self._outgoing = outgoing

    @property
    def uri(self) -> str:
        return self._uri

    @property
    def access_levels(self) -> list[ApiAccessLevelSuper]:
        return self._access_levels

    @property
    def access_type(self) -> Optional[ApiAccessType]:
        return self._access_type

    @property
    def category(self) -> Optional[ApiEndpointCategorySuper]:
        return self._category

    @property
    def outgoing(self) -> bool:
        return self._outgoing


class ApiURIsSuper:
    @classmethod
    def get_endpoints(cls) -> list[ApiEndpointDefinition]:
        return [getattr(cls, x) for x in cls.__dict__.keys() if isinstance(getattr(cls, x), ApiEndpointDefinition)]

    @classmethod
    def get_definition_for_uri(cls, value: str):
        for endpoint in cls.get_endpoints():
            if endpoint.uri == value:
                return endpoint
        raise ValueError(value)

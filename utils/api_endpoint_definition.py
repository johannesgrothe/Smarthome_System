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


class ApiURIs:
    affe = ApiEndpointDefinition("yolo", [], ApiAccessType.read)


if __name__ == "__main__":
    print(ApiURIs.affe.uri)
    print(ApiURIs.affe.access_type)

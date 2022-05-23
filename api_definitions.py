"""Collection of constants for all api uris"""

# This file was generated by 'api_constants_exporter.py' at 'https://github.com/johannesgrothe/Smarthome_System'
# Do not modify this file, modify 'api_docs/api_specs.json' and export.
# Every change made will be overwritten at next export.

import enum

try:
    from utils.api_endpoint_definition import ApiEndpointDefinition, ApiAccessType, ApiAccessLevelSuper, ApiURIsSuper
    from utils.software_version import SoftwareVersion
except ModuleNotFoundError:
    from .utils.api_endpoint_definition import ApiEndpointDefinition, ApiAccessType, ApiAccessLevelSuper, ApiURIsSuper
    from .utils.software_version import SoftwareVersion


# API Version
api_version = SoftwareVersion(1, 1, 2)


class ApiAccessLevel(ApiAccessLevelSuper, enum.IntEnum):
    """Container for all API access levels"""

    admin = 7  # Admin
    mqtt = 6  # MQTT
    user = 5  # User
    guest = 4  # Guest


class ApiURIs(ApiURIsSuper):
    """Container for all API URIs"""

    # URIs exposed by the bridge

    # Write Complete Config to Client
    client_config_write = ApiEndpointDefinition("config/write",
                                                [ApiAccessLevel.admin],
                                                ApiAccessType.write,
                                                False)

    # Delete Config
    client_config_delete = ApiEndpointDefinition("config/delete",
                                                 [ApiAccessLevel.admin],
                                                 ApiAccessType.write,
                                                 False)

    # Client Heartbeat
    heartbeat = ApiEndpointDefinition("heartbeat",
                                      [ApiAccessLevel.admin, ApiAccessLevel.mqtt],
                                      ApiAccessType.write,
                                      False)

    # Read Bridge Info
    info_bridge = ApiEndpointDefinition("info/bridge",
                                        [ApiAccessLevel.admin, ApiAccessLevel.user, ApiAccessLevel.guest],
                                        ApiAccessType.read,
                                        False)

    # Read Clients Info
    info_clients = ApiEndpointDefinition("info/clients",
                                         [ApiAccessLevel.admin, ApiAccessLevel.user, ApiAccessLevel.guest],
                                         ApiAccessType.read,
                                         False)

    # Read Gadgets Info
    info_gadgets = ApiEndpointDefinition("info/gadgets",
                                         [ApiAccessLevel.admin, ApiAccessLevel.user, ApiAccessLevel.guest],
                                         ApiAccessType.read,
                                         False)

    # Read Gadget Publisher Info
    info_gadget_publishers = ApiEndpointDefinition("info/gadget_publishers",
                                                   [ApiAccessLevel.admin, ApiAccessLevel.user],
                                                   ApiAccessType.read,
                                                   False)

    # Update Gadget
    update_gadget = ApiEndpointDefinition("update/gadget",
                                          [ApiAccessLevel.admin, ApiAccessLevel.mqtt, ApiAccessLevel.user],
                                          ApiAccessType.write,
                                          False)

    # Sync Client
    sync_client = ApiEndpointDefinition("sync/client",
                                        [ApiAccessLevel.admin, ApiAccessLevel.mqtt],
                                        ApiAccessType.write,
                                        False)

    # Reboot Client
    reboot_connected_client = ApiEndpointDefinition("reboot/client",
                                                    [ApiAccessLevel.admin, ApiAccessLevel.user],
                                                    ApiAccessType.write,
                                                    False)

    # Sync Event
    sync_event = ApiEndpointDefinition("sync/event",
                                       [ApiAccessLevel.admin, ApiAccessLevel.mqtt],
                                       ApiAccessType.write,
                                       False)

    # Test Echo
    test_echo = ApiEndpointDefinition("echo",
                                      [ApiAccessLevel.admin],
                                      ApiAccessType.write,
                                      False)

    # Retrieve all stored configs
    config_storage_get_all = ApiEndpointDefinition("config/storage/get_all",
                                                   [ApiAccessLevel.admin, ApiAccessLevel.user],
                                                   ApiAccessType.read,
                                                   False)

    # Retrieve stored config
    config_storage_get = ApiEndpointDefinition("config/storage/get",
                                               [ApiAccessLevel.admin, ApiAccessLevel.user],
                                               ApiAccessType.read,
                                               False)

    # Save config
    config_storage_save = ApiEndpointDefinition("config/storage/save",
                                                [ApiAccessLevel.admin],
                                                ApiAccessType.write,
                                                False)

    # Delete Config
    config_storage_delete = ApiEndpointDefinition("config/storage/delete",
                                                  [ApiAccessLevel.admin],
                                                  ApiAccessType.write,
                                                  False)

    # Bridge update check
    bridge_update_check = ApiEndpointDefinition("bridge/update/check",
                                                [ApiAccessLevel.admin],
                                                ApiAccessType.read,
                                                False)

    # Bridge update execute
    bridge_update_execute = ApiEndpointDefinition("bridge/update/execute",
                                                  [ApiAccessLevel.admin],
                                                  ApiAccessType.write,
                                                  False)

    # URIs exposed by the client

    # Write System Config
    client_system_config_write = ApiEndpointDefinition("config/system/write", [], None, True)

    # Write Event Config
    client_event_config_write = ApiEndpointDefinition("config/event/write", [], None, True)

    # Write Gadget Config
    client_gadget_config_write = ApiEndpointDefinition("config/gadget/write", [], None, True)

    # Reboot Client
    client_reboot = ApiEndpointDefinition("reboot/client", [], None, True)

    # Client Sync Request
    sync_request = ApiEndpointDefinition("sync", [], None, True)

    # Sync Event
    client_sync_event = ApiEndpointDefinition("sync/event", [], None, True)

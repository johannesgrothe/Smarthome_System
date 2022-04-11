#pragma once
// Collection of constants for all api uris

// This file was generated by 'api_constants_exporter.py' at 'https://github.com/johannesgrothe/Smarthome_System'
// Do not modify this file, modify 'api_docs/api_specs.json' and export.
// Every change made will be overwritten at next export.

#include <string>
#include <cstdint>

// Namespace for all api constants and definitions
namespace api_definitions {

    // API Version
    namespace version {
        constexpr uint8_t major = 1;
        constexpr uint8_t minor = 0;
        constexpr uint8_t bugfix = 11;
    }

    // Api URIs
    namespace uris {
        constexpr char heartbeat [] = "heartbeat";  // Client Heartbeat (Client -> Bridge)
        constexpr char update_gadget [] = "update/gadget";  // Update Gadget (Client -> Bridge)
        constexpr char sync_client [] = "sync/client";  // Sync Client (Client -> Bridge)
        constexpr char sync_event [] = "sync/event";  // Sync Event (Client -> Bridge)
        constexpr char client_system_config_write [] = "config/system/write";  // Write System Config (Bridge -> Client)
        constexpr char client_event_config_write [] = "config/event/write";  // Write Event Config (Bridge -> Client)
        constexpr char client_gadget_config_write [] = "config/gadget/write";  // Write Gadget Config (Bridge -> Client)
        constexpr char client_config_delete [] = "config/delete";  // Delete Config (Bridge -> Client)
        constexpr char client_update_gadget [] = "update/gadget";  // Update Gadget (Client -> Client)
        constexpr char client_reboot [] = "reboot/client";  // Reboot Client (Bridge -> Client)
        constexpr char sync_request [] = "sync";  // Client Sync Request (Bridge -> Client)
        constexpr char client_sync_event [] = "sync/event";  // Sync Event (Bridge -> Client)
        constexpr char test_echo [] = "echo";  // Test Echo (Bridge -> Client)
    }
}

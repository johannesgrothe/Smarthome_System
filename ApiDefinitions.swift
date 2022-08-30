// Collection of constants for all api uris

// This file was generated by 'constants_exporter_api_swift.py' at 'https://github.com/johannesgrothe/Smarthome_System'
// Do not modify this file, modify 'api_docs/api_specs.json' and 'gadget_docs/gadget_specs.json' and export.
// Every change made will be overwritten at next export.


let api_version = SoftwareVersion(major=1, minor=1, bugfix=3)


enum ApiURIs : String {
    case info_bridge = "info/bridge"   // Read Bridge Info
    case bridge_update_check = "bridge/update/check"   // Bridge update check
    case bridge_update_execute = "bridge/update/execute"   // Bridge update execute
    case bridge_add_user = "bridge/add_user"   // Add user to Bridge
    case info_gadgets = "info/gadgets"   // Read Gadgets Info
    case update_gadget = "update/gadget"   // Update Gadget
    case client_config_write = "config/write"   // Write Complete Config to Client
    case client_config_delete = "config/delete"   // Delete Config
    case info_clients = "info/clients"   // Read Clients Info
    case reboot_connected_client = "reboot/client"   // Reboot Client
    case info_gadget_publishers = "info/gadget_publishers"   // Read Gadget Publisher Info
    case config_storage_get_all = "config/storage/get_all"   // Retrieve all stored configs
    case config_storage_get = "config/storage/get"   // Retrieve stored config
    case config_storage_save = "config/storage/save"   // Save config
    case config_storage_delete = "config/storage/delete"   // Delete Config
}

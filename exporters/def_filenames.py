"""Module for exporter filename constants"""
import os

# Doc Files
FILE_API_SPECS = os.path.join("api_docs", "api_specs.json")
FILE_GADGET_SPECS = os.path.join("gadget_docs", "gadget_specs.json")
FILE_HW_VARIANTS = os.path.join("client_variants", "hw_variants.json")
FILE_SW_VARIANTS = os.path.join("client_variants", "sw_variants.json")

# Generated Files - Api
FILE_API_ACCESS_LEVELS = "api_access_levels.md"
FILE_API_BRIDGE = "api_endpoints_bridge.md"
FILE_API_CLIENT = "api_endpoints_client.md"
FILE_GADGET_CLASSES = "gadget_classes.md"
FILE_GADGETS_BRIDGE = "gadgets_local.md"
FILE_GADGETS_CLIENT = "gadgets_remote.md"

# Generated files - Constants
FILE_API_CONSTANTS_PY = "api_definitions.py"
FILE_API_CONSTANTS_CPP = "api_definitions.h"
FILE_API_CONSTANTS_JS = "api_definitions.js"
FILE_API_CONSTANTS_SWIFT = "ApiDefinitions.swift"

FILE_GADGET_CONSTANTS_PY = "gadget_definitions.py"
FILE_GADGET_CONSTANTS_CPP = "gadget_definitions.h"
FILE_GADGET_CONSTANTS_JS = "gadget_definitions.js"
FILE_GADGET_CONSTANTS_SWIFT = "GadgetDefinitions.swift"

# Generated files - Variants
FILE_VARIANTS_CPP = "variants.cpp"
FILE_VARIANTS_JS = "variants.js"
FILE_VARIANTS_PY = "variants.py"
FILE_VARIANTS_SWIFT = "Variants.swift"

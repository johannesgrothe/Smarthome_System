import os

# Base path of github repo for file links
GITHUB_BASE_FILE_URI = "https://github.com/johannesgrothe/Smarthome_System/blob/master/"

# Name of the file containing the api definitions
PATH_API_SPECS = os.path.join("api_docs", "api_specs.json")

# Name of the file containing the api definitions
PATH_GADGET_SPECS = os.path.join("gadget_docs", "gadget_specs.json")

# Path to the json schemas referenced in the api specs file
PATH_JSON_SCHEMAS = "json_schemas"

# Path to the exported api constants files (Ending is supplied by the individual exporters)
PATH_FILE_API_CONSTANTS = "api_definitions"

# Path to the exported api constants files (Ending is supplied by the individual exporters)
PATH_FILE_GADGET_CONSTANTS = "gadget_definitions"

# Path to the exported api documentation markdown
NAME_FILE_API_DOCS = "api.md"

# Path to the exported gadget documentation markdown
NAME_FILE_GADGET_DOCS = "gadgets.md"

# Path to temporary generated files
PATH_TEMP_DIR = "temp"

# Namespace api docs
CPP_NAMESPACE_API_DOCS = "api_definitions"

# Namespace for api URIs
CPP_NAMESPACE_API_URIS = "uris"

# Namespace for api version
CPP_NAMESPACE_API_VERSION = "version"

# Classname for api URIs
PY_CLASSNAME_URIS = "ApiURIs"

# Namespace api docs
PY_VARNAME_API_VERSION = "api_version"

# Namespace for gadget specification
CPP_NAMESPACE_GADGET_DOCS = "gadget_definitions"

# Classname for JS gadget specification
JS_CLASSNAME_GADGET_SPECS = "GadgetDefinitions"

# Classname for JS API constants
JS_CLASSNAME_API = "ApiConstants"

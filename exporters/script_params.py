import os

# Name of the file containing the api definitions
PATH_API_SPECS = os.path.join("api_docs", "api_specs.json")

# Name of the file containing the api definitions
PATH_GADGET_SPECS = os.path.join("gadget_docs", "gadget_specs.json")

# Path to the json schemas referenced in the api specs file
PATH_JSON_SCHEMAS = "json_schemas"

# Path to the exported api constants files (Ending is supplied by the individual exporters)
PATH_FILE_API_CONSTANTS = "api_params"

# Path to the exported api constants files (Ending is supplied by the individual exporters)
PATH_FILE_GADGET_CONSTANTS = "gadget_definitions"

# Path to the exported api documentation markdown
NAME_FILE_API_DOCS = "api.md"

# Path to the exported gadget documentation markdown
NAME_FILE_GADGET_DOCS = "gadgets.md"

# Path to temporary generated files
PATH_TEMP_DIR = "temp"

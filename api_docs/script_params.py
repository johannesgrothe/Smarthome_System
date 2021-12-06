import os

# Path to the file containing the api definitions
PATH_API_SPECS = "api_specs.json"

# Path to the json schemas referenced in the api specs file
PATH_JSON_SCHEMAS = os.path.join("..", "json_schemas")

# Path to the exported api constants files (Ending is supplied by the individual exporters)
PATH_FILE_CONSTANTS = os.path.join(os.pardir, "api_params")

# Path to the exported api documentation markdown
NAME_FILE_DOCS = "api.md"

# Path to temporary generated files
PATH_TEMP_DIR = os.path.join(os.pardir, "temp")

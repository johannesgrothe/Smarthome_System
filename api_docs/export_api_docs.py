"""Module for the api doc exporter"""

import sys
import os
import json
from jsonschema import validate, ValidationError
import logging

sys.path.append("..")

# from markdown_file import MarkdownFile
from utils.markdown_file import *

# Path to the file containing the api definitions
_path_api_specs = "api_docs/api_specs.json"

# Path to the json schemas referenced in the api specs file
_path_json_schemas = "json_schemas"


class ApiDocExporter:
    """Class that handles the api doc exporting process"""

    _definitions_file: str
    _schema_folder: str

    _api_definition: dict
    _logger: logging.Logger

    def __init__(self, definitions: str, schemas: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._definitions_file = definitions
        self._schema_folder = schemas
        try:
            self._load_api_definition()
        except ValidationError as err:
            self._logger.error(err.args[0])
            raise Exception("Could not load api definition because of failed schema validation")
        self._logger.info("Api definitions loaded successfully")

    def _load_api_definition(self):
        with open(self._definitions_file, "r") as file_p:
            data = json.load(file_p)

        schema_path = os.path.abspath(os.path.join(self._definitions_file, os.pardir, data["$schema"]))

        with open(schema_path, "r") as file_p:
            schema = json.load(file_p)

        validate(data, schema)
        self._api_definition = data

    def export_api_doc(self, out_file: str):
        file = MarkdownFile()

        file.save(out_file)


def main():
    exporter = ApiDocExporter(_path_api_specs, _path_json_schemas)
    if not os.path.isdir("temp"):
        os.mkdir("temp")
    exporter.export_api_doc("temp/out.md")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()

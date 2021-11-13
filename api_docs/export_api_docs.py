"""Module for the api doc exporter"""

import sys
import os
import json
from jsonschema import validate, ValidationError
import logging

sys.path.append("..")

# from markdown_file import MarkdownFile
from utils.markdown_file import *
from utils.json_schema_formatter import JsonSchemaFormatter
from utils.schema_loader import SchemaLoader

# Path to the file containing the api definitions
_path_api_specs = "api_docs/api_specs.json"

# Path to the json schemas referenced in the api specs file
_path_json_schemas = "json_schemas"


class ApiDocExporter:
    """Class that handles the api doc exporting process"""

    _definitions_file: str
    _schema_folder: str

    _api_definition: dict
    _schema_data: dict
    _logger: logging.Logger

    def __init__(self, definitions: str, schemas: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._definitions_file = definitions
        self._schema_folder = schemas
        self._schema_data = SchemaLoader(schemas).load_schemas()
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

    def _read_schema(self, schema: str) -> str:
        if schema.endswith(".json"):
            schema = schema[:-5]
        return JsonSchemaFormatter.shorten_schema(self._schema_data[schema])

    @staticmethod
    def _format_list(data: list[str], default: str) -> str:
        if not data:
            return default
        else:
            return ", ".join(data)

    def export_api_doc(self, out_file: str):
        file = MarkdownFile()
        file.add(MarkdownHeader(self._api_definition["title"], 0))
        file.add(MarkdownText(self._api_definition["description"]))
        for mapping in self._api_definition["mappings"]:
            map_data = self._api_definition["mappings"][mapping]
            file.add(MarkdownHeader(map_data["title"], 2))
            file.add(MarkdownText(map_data["description"]))

            status_table = MarkdownTable(["Option", "Value"])
            status_table.add_line(["Broadcast Allowed", ('Yes' if map_data['broadcast_allowed'] else 'No')])
            status_table.add_line(["Sender", self._format_list(map_data['sender'], "Anybody")])
            status_table.add_line(["Receiver", self._format_list(map_data['receiver'], "Anybody")])

            file.add(status_table)

            file.add(MarkdownHeader("Request", 3))
            req_data = map_data["request"]
            file.add(MarkdownText(req_data["comment"]))
            req_schema = self._read_schema(req_data["schema"])
            file.add(MarkdownCode(req_schema, language="json"))

            file.add(MarkdownHeader("Response", 3))
            res_data = map_data["response"]
            file.add(MarkdownText(res_data["comment"]))
            if res_data["schema"] is not None:
                res_schema = self._read_schema(res_data["schema"])
                file.add(MarkdownCode(res_schema, language="json"))
            file.add(MarkdownDivider())

        file.save(out_file)


def main():
    exporter = ApiDocExporter(_path_api_specs, _path_json_schemas)
    if not os.path.isdir("temp"):
        os.mkdir("temp")
    exporter.export_api_doc("temp/api_documentation.md")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()

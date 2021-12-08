"""Module for the api doc exporter"""
import logging
import sys
from script_params import *
from api_loader import ApiLoader

# Needed for execution when included as submodule
sys.path.append("../")

from utils.markdown_file import *
from utils.json_schema_formatter import JsonSchemaFormatter
from utils.schema_loader import SchemaLoader

# Base path for the links to the actual json schema files
_schema_link_base_path = "https://github.com/johannesgrothe/Smarthome_System/blob/master/json_schemas/"


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
        self._api_definition = ApiLoader(self._definitions_file).get_definitions()
        self._logger.info("Api definitions loaded successfully")

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

        file.add(MarkdownDivider())
        file.add(MarkdownHeader("Table of Contents", 1))
        for mapping in self._api_definition["mappings"]:
            map_data = self._api_definition["mappings"][mapping]
            target: str = map_data["title"].lower().replace(" ", "-")
            file.add(MarkdownInternalLink(map_data["title"], target))
        file.add(MarkdownDivider())

        for mapping in self._api_definition["mappings"]:
            map_data = self._api_definition["mappings"][mapping]
            file.add(MarkdownHeader(map_data["title"], 2))
            file.add(MarkdownText(map_data["description"]))

            status_table = MarkdownTable(["Option", "Value"])
            status_table.add_line(["Broadcast Allowed", ('Yes' if map_data['broadcast_allowed'] else 'No')])
            status_table.add_line(["Sender", self._format_list(map_data['sender'], "Anybody")])
            status_table.add_line(["Receiver", self._format_list(map_data['receiver'], "Anybody")])
            http_method = "No HTTP Allowed" if not map_data['http_method'] else map_data['http_method']
            status_table.add_line(["HTTP Method", http_method])

            file.add(status_table)

            file.add(MarkdownCode(map_data["uri"]["value"], language="json", block=False))

            file.add(MarkdownHeader("Request", 3))
            req_data = map_data["request"]
            file.add(MarkdownText(req_data["comment"]))
            file.add(MarkdownHyperLink(req_data['schema'], f"{_schema_link_base_path}{req_data['schema']}", "Schema: "))
            req_schema = self._read_schema(req_data["schema"])
            file.add(MarkdownCode(req_schema, language="json"))

            file.add(MarkdownHeader("Response", 3))
            res_data = map_data["response"]
            file.add(MarkdownText(res_data["comment"]))
            if res_data["schema"] is not None:
                file.add(
                    MarkdownHyperLink(res_data['schema'], f"{_schema_link_base_path}{res_data['schema']}", "Schema: "))
                res_schema = self._read_schema(res_data["schema"])
                file.add(MarkdownCode(res_schema, language="json"))
            file.add(MarkdownDivider())

        file.save(out_file)


def main():
    exporter = ApiDocExporter(PATH_API_SPECS, PATH_JSON_SCHEMAS)
    if not os.path.isdir(PATH_TEMP_DIR):
        os.mkdir(PATH_TEMP_DIR)
    exporter.export_api_doc(os.path.join(PATH_TEMP_DIR, "api.md"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()

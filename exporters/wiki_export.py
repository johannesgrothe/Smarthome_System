import logging
import os

from system.exporters.definitions_loader import DefinitionsLoader
from system.exporters.script_params import GITHUB_BASE_FILE_URI, PATH_FILE_API_CONSTANTS
from system.utils.json_schema_formatter import JsonSchemaFormatter
from system.utils.markdown_file import *

# Base path for the links to the actual json schema files
from system.utils.schema_loader import SchemaLoader

_schema_link_base_path = "https://github.com/johannesgrothe/Smarthome_System/blob/master/json_schemas/"

_api_specs_file = os.path.join("api_docs", "api_specs.json")
_gadget_specs_file = os.path.join("gadget_docs", "gadget_specs.json")
_schema_folder = "json_schemas"


class WikiExporter:
    _gadget_class_def: dict
    _gadgets_local: dict
    _gadgets_remote: dict

    _api_access_level_def: dict
    _api_endpoint_def: dict
    _api_version: str
    _schema_data: dict

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

        gadget_def = DefinitionsLoader(_gadget_specs_file).get_definitions()
        self._gadget_class_def = gadget_def["gadget_classes"]
        self._gadgets_local = gadget_def["gadget_definitions"]["bridge_gadgets"]
        self._gadgets_remote = gadget_def["gadget_definitions"]["client_gadgets"]

        api_def = DefinitionsLoader(_api_specs_file).get_definitions()
        self._api_endpoint_def = api_def["endpoints"]
        self._api_access_level_def = api_def["access_levels"]
        self._api_version = api_def["version"]

        self._schema_data = SchemaLoader(_schema_folder).load_schemas()

    @staticmethod
    def _add_exported_libraries(base_filename: str, file: MarkdownFile):
        language_info = [("C++", "h"), ("Python", "py"), ("JavaScript", "js"), ("Swift", "swift")]
        file.add(MarkdownHeader("Exported Code Libraries", 2))
        buf_table = MarkdownTable(["Language", "Link"])
        for language, ending in language_info:
            filename = f"{base_filename}.{ending}"
            link = MarkdownHyperLink(filename, f"{GITHUB_BASE_FILE_URI}{filename}")
            buf_table.add_line([language, link])
        file.add(buf_table)

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

    @staticmethod
    def _format_access_levels(data: list[str], default: str) -> str:
        if not data:
            return default
        else:
            return ", ".join(data)

    @staticmethod
    def _format_sender(sender: str) -> str:
        switcher = {
            "bridge": "Bridge",
            "client": "Client",
            "web_application": "Web Application"
        }
        return switcher.get(sender)

    @abstractmethod
    def export(self, filename: str):
        pass


class WikiExporterApiEndpoints(WikiExporter, ABC):

    def _export_mapping(self, map_data: dict, file: MarkdownFile, receiver: str, title_level: int):
        file.add(MarkdownHeader(map_data["title"], title_level))
        file.add(MarkdownText(map_data["description"]))

        file.add(MarkdownCode(map_data["uri"]["value"], language="json", block=False))

        status_table = MarkdownTable(["Option", "Value"])
        status_table.add_line(["Broadcast Allowed", ('Yes' if map_data['broadcast_allowed'] else 'No')])
        status_table.add_line(["Sender", self._format_list([self._format_sender(x) for x in map_data['sender']],
                                                           "Anybody")])
        status_table.add_line(["Receiver", self._format_sender(receiver)])

        if "access_type" in map_data:
            access_type = "Read" if map_data["access_type"] == "read" else "Write"
            http_method = "GET" if map_data["access_type"] == "read" else "POST"

            status_table.add_line(["Access Type", access_type])
            status_table.add_line(["HTTP Method", http_method])

        file.add(status_table)

        if "access_level" in map_data:
            file.add(MarkdownHeader("Access Levels", title_level + 1))
            file.add(MarkdownText("Access levels required to access this ressource"))
            access_level_list = MarkdownList()
            for access_level in map_data["access_level"]:
                level_name = self._api_access_level_def["items"][access_level]["name"]
                access_level_list.add_line(MarkdownInternalLinkGithub(level_name, level_name))
            file.add(access_level_list)

        file.add(MarkdownHeader("Request", title_level + 1))
        req_data = map_data["request"]
        file.add(MarkdownText(req_data["comment"]))
        file.add(MarkdownHyperLink(req_data['schema'], f"{_schema_link_base_path}{req_data['schema']}", "Schema: "))
        req_schema = self._read_schema(req_data["schema"])
        file.add(MarkdownCode(req_schema, language="json"))

        file.add(MarkdownHeader("Response", title_level + 1))
        res_data = map_data["response"]
        file.add(MarkdownText(res_data["comment"]))
        if res_data["schema"] is not None:
            file.add(
                MarkdownHyperLink(res_data['schema'], f"{_schema_link_base_path}{res_data['schema']}", "Schema: "))
            res_schema = self._read_schema(res_data["schema"])
            file.add(MarkdownCode(res_schema, language="json"))
        file.add(MarkdownDivider())


class WikiExporterGadgets(WikiExporter, ABC):

    @staticmethod
    def _gen_enum_table(data: dict) -> MarkdownTable:
        overview = {}
        for key, data in data.items():
            val = data["enum_value"]
            if val in overview:
                raise Exception(f"Double Identifier: {val}")
            overview[val] = key
        key_list = [x for x in overview.keys()]
        key_list.sort()

        status_table = MarkdownTable(["Int Identifier", "String Identifier"])
        for key in key_list:
            status_table.add_line([str(key), overview[key]])
        return status_table

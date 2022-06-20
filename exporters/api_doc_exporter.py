"""Module for the api doc exporter"""
from exporters.doc_exporter import DocExporter
from exporters.script_params import PATH_FILE_API_CONSTANTS
from utils.markdown_file import *
from utils.json_schema_formatter import JsonSchemaFormatter
from utils.schema_loader import SchemaLoader

# Base path for the links to the actual json schema files
_schema_link_base_path = "https://github.com/johannesgrothe/Smarthome_System/blob/master/json_schemas/"


class ApiDocExporter(DocExporter):
    """Class that handles the api doc exporting process"""

    _schema_folder: str
    _schema_data: dict

    def __init__(self, definitions: str, schemas: str):
        super().__init__(definitions)
        self._schema_folder = schemas
        self._schema_data = SchemaLoader(schemas).load_schemas()

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
                level_name = self._definitions["access_level"][access_level]["name"]
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

    def export_docs(self, out_file: str):
        file = MarkdownFile()
        file.add(MarkdownHeader(self._definitions["title"], 0))
        file.add(MarkdownText(self._definitions["description"]))
        file.add(MarkdownText("Latest Api Version: " + self._definitions["version"]))

        file.add(MarkdownDivider())
        self._add_exported_libraries(PATH_FILE_API_CONSTANTS, file)
        file.add(MarkdownDivider())

        file.add(MarkdownHeader("Access Levels", 1))
        for _, data in self._definitions["access_level"].items():
            file.add(MarkdownHeader(data["name"], 2))
            file.add(MarkdownText(data["description"]))
            status_table = MarkdownTable(["Option", "Value"])
            status_table.add_line(["Int Identifier", data["id"]])
            status_table.add_line(["Variable Name", data["var_name"]])
            file.add(status_table)

        file.add(MarkdownDivider())

        file.add(MarkdownHeader("Bridge URIs", 1))
        for category, cat_data in self._definitions["mappings"]["bridge"].items():
            cat_name = cat_data["name"]
            file.add(MarkdownHeader(cat_name, 2))
            file.add(MarkdownText(cat_data["description"]))
            for _, map_data in cat_data["endpoints"].items():
                self._export_mapping(map_data, file, "bridge", 3)

        file.add(MarkdownHeader("Client URIs", 1))
        for _, map_data in self._definitions["mappings"]["client"].items():
            self._export_mapping(map_data, file, "client", 3)

        file.save(out_file)

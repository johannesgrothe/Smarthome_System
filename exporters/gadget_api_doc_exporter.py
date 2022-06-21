import json

from exporters.doc_exporter import DocExporter
from exporters.script_params import PATH_FILE_GADGET_CONSTANTS
from utils.markdown_file import *

from system.utils.json_schema_formatter import JsonSchemaFormatter
from system.utils.schema_loader import SchemaLoader


class GadgetApiDocExporter(DocExporter):
    """Class that handles the gadget doc exporting process"""

    _schema_data: dict

    def __init__(self, definitions: str, schemas: str):
        super().__init__(definitions)
        self._schema_data = SchemaLoader(schemas).load_schemas()

    def _read_schema(self, schema: str) -> str:
        if schema.endswith(".json"):
            schema = schema[:-5]
        return JsonSchemaFormatter.shorten_schema(self._schema_data[schema])

    def export_docs(self, out_file: str):
        file = MarkdownFile()
        file.add(MarkdownHeader(self._definitions["gadget_classes"]["title"], 0))
        file.add(MarkdownText(self._definitions["gadget_classes"]["description"]))

        file.add(MarkdownDivider())
        self._add_exported_libraries(PATH_FILE_GADGET_CONSTANTS, file)
        file.add(MarkdownDivider())

        for _, gadget_class in self._definitions["gadget_classes"]["items"].items():
            file.add(MarkdownHeader(gadget_class["name"], 1))
            file.add(MarkdownText(gadget_class["description"]))

            identifier_table = MarkdownTable(["Parameter Name", "Parameter Value"])
            identifier_table.add_line(["Int Identifier", str(gadget_class['enum_value'])])
            file.add(identifier_table)

            file.add(MarkdownHeader("Gadget Properties", 2))
            if gadget_class["attributes"]:
                file.add(MarkdownText("All properties of this Gadget"))
                attr_schema = self._read_schema(gadget_class["attributes"])
                file.add(MarkdownCode(attr_schema, language="json"))
            else:
                file.add(MarkdownText("No information available"))

            file.add(MarkdownHeader("Updatable Properties", 2))
            if gadget_class["sync_attributes"]:
                file.add(MarkdownText("All properties that can be updated"))
                update_schema = self._read_schema(gadget_class["sync_attributes"])
                file.add(MarkdownCode(update_schema, language="json"))
            else:
                file.add(MarkdownText("No information available"))

            file.add(MarkdownDivider())

        file.save(out_file)

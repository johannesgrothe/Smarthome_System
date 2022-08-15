from exporters.wiki_export import WikiExporter
from utils.markdown_file import *


class WikiExporterGadgetClasses(WikiExporter):
    def export(self, filename: str):
        file = MarkdownFile()
        file.add(MarkdownHeader(self._gadget_class_def["title"], 0))
        file.add(MarkdownText(self._gadget_class_def["description"]))

        for _, gadget_class in self._gadget_class_def["items"].items():
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

        file.save(filename)

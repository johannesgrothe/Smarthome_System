from system.exporters.wiki_export import WikiExporter
from system.utils.markdown_file import *


class WikiExporterApiAccessLevels(WikiExporter):
    def export(self, filename: str):
        file = MarkdownFile()
        file.add(MarkdownHeader(self._api_access_level_def["title"], 1))
        file.add(MarkdownText(self._api_access_level_def["description"]))
        file.add(MarkdownText("Latest Api Version: " + str(self._api_version)))

        for _, data in self._api_access_level_def["items"].items():
            file.add(MarkdownHeader(data["name"], 2))
            file.add(MarkdownText(data["description"]))
            status_table = MarkdownTable(["Option", "Value"])
            status_table.add_line(["Int Identifier", data["id"]])
            status_table.add_line(["Variable Name", data["var_name"]])
            file.add(status_table)

        file.save(filename)

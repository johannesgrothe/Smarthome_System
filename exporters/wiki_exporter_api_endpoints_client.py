import os
from system.exporters.wiki_export import WikiExporterApiEndpoints
from system.utils.markdown_file import *

_api_specs_file = os.path.join("api_docs", "api_specs.json")
_gadget_specs_file = os.path.join("gadget_docs", "gadget_specs.json")


class WikiExporterApiEndpointsClient(WikiExporterApiEndpoints):
    def export(self, target_file: str):
        file = MarkdownFile()
        file.add(MarkdownHeader(self._api_endpoint_def["title"], 1))
        file.add(MarkdownText(self._api_endpoint_def["description"]))
        file.add(MarkdownText("Latest Api Version: " + str(self._api_version)))

        for _, map_data in self._api_endpoint_def["items"]["client"].items():
            self._export_mapping(map_data, file, "client", 2)

        file.save(target_file)

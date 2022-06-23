import logging
import os

from system.exporters.definitions_loader import DefinitionsLoader
from system.exporters.script_params import GITHUB_BASE_FILE_URI, PATH_FILE_API_CONSTANTS
from system.exporters.wiki_export import WikiExporter, WikiExporterApiEndpoints
from system.utils.markdown_file import *

_api_specs_file = os.path.join("api_docs", "api_specs.json")
_gadget_specs_file = os.path.join("gadget_docs", "gadget_specs.json")


class WikiExporterApiEndpointsBridge(WikiExporterApiEndpoints):
    def export(self, target_file: str):
        file = MarkdownFile()
        file.add(MarkdownHeader(self._api_endpoint_def["title"], 1))
        file.add(MarkdownText(self._api_endpoint_def["description"]))
        file.add(MarkdownText("Latest Api Version: " + self._api_version))

        for category, cat_data in self._api_endpoint_def["items"]["bridge"].items():
            cat_name = cat_data["name"]
            file.add(MarkdownHeader(cat_name, 2))
            file.add(MarkdownText(cat_data["description"]))
            for _, map_data in cat_data["endpoints"].items():
                self._export_mapping(map_data, file, "bridge", 3)

        file.save(target_file)

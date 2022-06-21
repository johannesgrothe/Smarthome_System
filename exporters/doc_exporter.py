import logging
from abc import abstractmethod

from exporters.definitions_loader import DefinitionsLoader
from exporters.script_params import GITHUB_BASE_FILE_URI
from utils.markdown_file import MarkdownHyperLink, MarkdownTable, MarkdownHeader, MarkdownFile


class DocExporter:

    _logger: logging.Logger
    _definitions_file: str
    _definitions: dict

    def __init__(self, definitions: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._definitions_file = definitions
        self._definitions = DefinitionsLoader(self._definitions_file).get_definitions()
        self._logger.info("Definitions loaded successfully")

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

    @abstractmethod
    def export_docs(self, out_file: str):
        pass

from exporters.doc_exporter import DocExporter
from utils.markdown_file import *


class GadgetDocExporter(DocExporter):
    """Class that handles the gadget doc exporting process"""

    def __init__(self, definitions: str):
        super().__init__(definitions)

    def export_docs(self, out_file: str):
        file = MarkdownFile()
        file.add(MarkdownHeader(self._definitions["title"], 0))
        file.add(MarkdownText(self._definitions["description"]))

        file.add(MarkdownDivider())
        file.add(MarkdownHeader("Table of Contents", 1))

        file.save(out_file)

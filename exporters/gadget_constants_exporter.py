"""Module for the gadget constants exporter"""
from exporters.constants_exporter import ConstantsExporter

_export_file_docstring = "Collection of constants for all gadgets and characteristics"


class GadgetConstantsExporter(ConstantsExporter):
    """Class that handles the gadget doc exporting process"""

    _api_definition: dict

    def __init__(self, definitions: str):
        super().__init__(definitions)

    def export_python(self, out_file: str):
        lines = self._generate_python_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

    def export_cpp(self, out_file: str):
        lines = self._generate_cpp_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

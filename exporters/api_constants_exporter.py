"""Module for the api constants exporter"""
from exporters.constants_exporter import ConstantsExporter

_export_file_docstring = "Collection of constants for all api uris"


class ApiConstantsExporter(ConstantsExporter):
    """Class that handles the api doc exporting process"""

    def __init__(self, definitions: str):
        super().__init__(definitions)

    def export_python(self, out_file: str):
        lines = self._generate_python_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        for mapping in self._definition["mappings"]:
            data = self._definition["mappings"][mapping]
            lines.append(f"# {data['title']}")
            lines.append(f"{data['uri']['var_name']} = \"{data['uri']['value']}\"")
            lines.append("")

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

    def export_cpp(self, out_file: str):
        lines = self._generate_cpp_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        for mapping in self._definition["mappings"]:
            data = self._definition["mappings"][mapping]
            lines.append(f"// {data['title']}")
            lines.append(f"#define {data['uri']['var_name']} \"{data['uri']['value']}\"")
            lines.append("")

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

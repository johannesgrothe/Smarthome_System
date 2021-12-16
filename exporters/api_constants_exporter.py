"""Module for the api constants exporter"""
from exporters.script_params import *
from exporters.constants_exporter import ConstantsExporter
from utils.software_version import SoftwareVersion

_export_file_docstring = "Collection of constants for all api uris"


class ApiConstantsExporter(ConstantsExporter):
    """Class that handles the api doc exporting process"""

    def __init__(self, definitions: str):
        super().__init__(definitions)

    def export_python(self, out_file: str):
        lines = self._generate_python_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        for x in self._generate_python_imports([("utils.system_identifier", "StringSystemIdentifier"),
                                                ("utils.software_version", "SoftwareVersion")]):
            lines.append(x)

        lines.append("")
        lines.append("")

        lines.append("# API Version")
        version = SoftwareVersion.from_string(self._definitions["version"])
        lines.append(f"{PY_VARNAME_API_VERSION} = SoftwareVersion({version.major}, {version.minor}, {version.bugfix})")

        lines.append("")
        lines.append("")

        lines.append(f"class {PY_CLASSNAME_URIS}(StringSystemIdentifier):")
        lines.append(f"    \"\"\"Container for all API URIs\"\"\"")
        lines.append("")

        for mapping, data in self._definitions["mappings"].items():
            lines.append(f"    {data['uri']['var_name']} = \"{data['uri']['value']}\"  # {data['title']}")

        lines.append("")

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

    def export_cpp(self, out_file: str):
        lines = self._generate_cpp_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]))

        lines.append("")
        lines.append("#include <string>")
        lines.append("")

        lines.append("// Namespace for all gadget and characteristic definitions")
        lines.append("namespace " + CPP_NAMESPACE_API_DOCS + " {")

        version = SoftwareVersion.from_string(self._definitions["version"])
        lines.append("")
        lines.append("    // API Version")
        lines.append("    namespace " + CPP_NAMESPACE_API_VERSION + " {")
        lines.append(f"        constexpr uint8_t major = {version.major};")
        lines.append(f"        constexpr uint8_t minor = {version.minor};")
        lines.append(f"        constexpr uint8_t bugfix = {version.bugfix};")
        lines.append("    }")
        lines.append("")

        lines.append("    // Api URIs")
        lines.append("    namespace " + CPP_NAMESPACE_API_URIS + " {")
        for index, (key, data) in enumerate(self._definitions["mappings"].items()):
            lines.append(f"        constexpr std::string {data['uri']['var_name']} = \"{data['uri']['value']}\";  // {data['title']}")
        lines.append("    }")
        lines.append("}")

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

"""Module for the api constants exporter"""
from exporters.script_params import *
from exporters.constants_exporter import ConstantsExporter
from utils.software_version import SoftwareVersion
from utils.cpp_file import *
from utils.js_file import *

_export_file_docstring = "Collection of constants for all api uris"


class ApiConstantsExporter(ConstantsExporter):
    """Class that handles the api doc exporting process"""

    def __init__(self, definitions: str):
        super().__init__(definitions)

    def _export_definition(self, data: dict, access_levels_data: dict, linebreak: bool) -> list[str]:
        if "access_level" in data:
            access_level_buffer = [access_levels_data[x]["var_name"] for x in access_levels_data if x in data["access_level"]]
            access_levels = f"[{', '.join([f'{PY_CLASSNAME_ACCESS_LEVEL}.{x}' for x in access_level_buffer])}]"
        else:
            access_levels = "[]"

        if linebreak:
            indent = "\n" + " " * (len(data['uri']['var_name']) + len(PY_CLASSNAME_API_DEFINITION_CONTAINER) + 8)
        else:
            indent = " "

        lines = [""]
        uri = data['uri']['value']
        access_type = f"{PY_CLASSNAME_ACCESS_TYPE}.{data['access_type']}" if "access_type" in data else "None"

        lines.append(f"    # {data['title']}")
        lines.append(
            f"    {data['uri']['var_name']} = {PY_CLASSNAME_API_DEFINITION_CONTAINER}(\"{uri}\",{indent}{access_levels},{indent}{access_type})")
        return lines

    def export_python(self, out_file: str):
        lines = self._generate_python_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        lines.append("import enum")
        lines.append("")

        for x in self._generate_python_imports([("utils.api_endpoint_definition",
                                                 f"{PY_CLASSNAME_API_DEFINITION_CONTAINER}, {PY_CLASSNAME_ACCESS_TYPE}, {PY_CLASSNAME_ACCESS_TYPE_SUPER}"),
                                                ("utils.software_version", "SoftwareVersion")]):
            lines.append(x)

        lines.append("")
        lines.append("")

        lines.append("# API Version")
        version = SoftwareVersion.from_string(self._definitions["version"])
        lines.append(f"{PY_VARNAME_API_VERSION} = SoftwareVersion({version.major}, {version.minor}, {version.bugfix})")

        lines.append("")
        lines.append("")

        lines.append(f"class {PY_CLASSNAME_ACCESS_LEVEL}({PY_CLASSNAME_ACCESS_TYPE_SUPER}, enum.IntEnum):")
        lines.append(f"    \"\"\"Container for all API access levels\"\"\"")
        lines.append("")

        access_level_data = self._definitions["access_level"]
        for mapping, data in access_level_data.items():
            lines.append(f"    {data['var_name']} = {data['id']}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append(f"class {PY_CLASSNAME_URIS}:")
        lines.append(f"    \"\"\"Container for all API URIs\"\"\"")
        lines.append("")
        lines.append("    # URIs exposed by the bridge")
        for _, data in self._definitions["mappings"]["bridge"].items():
            lines += self._export_definition(data, access_level_data, True)

        lines.append("")
        lines.append("    # URIs exposed by the client")
        for _, data in self._definitions["mappings"]["client"].items():
            if "bridge" in data["sender"]:
                lines += self._export_definition(data, access_level_data, False)

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

    def export_cpp(self, out_file: str):

        # Filter data to only export api constants relevant to the client
        filtered_data = []
        for key, data in self._definitions["mappings"]["bridge"].items():
            if "client" in data["sender"]:
                data["receiver"] = "bridge"
                filtered_data.append(data)
        for key, data in self._definitions["mappings"]["client"].items():
            data["receiver"] = "client"
            filtered_data.append(data)

        file = CppFile()

        self._add_cpp_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]), file)

        file.add(CppImport("string", in_package=False))
        file.add(CppImport("cstdint", in_package=False))

        package_namespace = CppNamespace(CPP_NAMESPACE_API_DOCS,
                                         "Namespace for all api constants and definitions")

        version = SoftwareVersion.from_string(self._definitions["version"])
        version_namespace = CppNamespace(CPP_NAMESPACE_API_VERSION,
                                         "API Version")
        version_namespace.add(CppVariable("constexpr uint8_t", "major", version.major))
        version_namespace.add(CppVariable("constexpr uint8_t", "minor", version.minor))
        version_namespace.add(CppVariable("constexpr uint8_t", "bugfix", version.bugfix))

        package_namespace.add(version_namespace)

        uri_namespace = CppNamespace(CPP_NAMESPACE_API_URIS,
                                     "Api URIs")
        for data in filtered_data:
            sender = "Client" if "client" in data['sender'] else "Bridge"
            receiver = "Bridge" if data['receiver'] == "bridge" else "Client"
            comment = data['title'] + f" ({sender} -> {receiver})"
            uri_namespace.add(CppVariable("constexpr char []",
                                          data['uri']['var_name'],
                                          data['uri']['value'],
                                          comment))

        package_namespace.add(uri_namespace)

        file.add(package_namespace)

        file.save(out_file)

    def export_js(self, out_file: str):

        # Filter data to only export api constants relevant to the web interface
        filtered_data = []
        for key, data in self._definitions["mappings"]["bridge"].items():
            if "web_application" in data["sender"]:
                data["receiver"] = "bridge"
                filtered_data.append(data)

        file = JSFile()

        self._add_js_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]), file)

        api_constants_class = JSConstantsClass(JS_CLASSNAME_API,
                                               "Class for all API constants and definitions")

        api_constants_class.add(JSBlankLine())

        version = SoftwareVersion.from_string(self._definitions["version"])
        api_constants_class.add(JSComment("API Version"))

        api_constants_class.add(JSVariable("static", "version_major", version.major))
        api_constants_class.add(JSVariable("static", "version_minor", version.minor))
        api_constants_class.add(JSVariable("static", "version_bugfix", version.bugfix))

        api_constants_class.add(JSBlankLine())

        api_constants_class.add(JSComment("API URIs"))

        for data in filtered_data:
            sender = "Web Application" if "web_application" in data['sender'] else "Bridge"
            receiver = "Bridge" if data['receiver'] == "bridge" else "Web Application"
            comment = data['title'] + f" ({sender} -> {receiver})"
            api_constants_class.add(JSVariable("static",
                                               "uri_" + data['uri']['var_name'],
                                               data['uri']['value'],
                                               comment))

        file.add(api_constants_class)

        file.save(out_file)

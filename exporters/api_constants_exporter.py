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

    def export_python(self, out_file: str):
        lines = self._generate_python_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        for x in self._generate_python_imports([("utils.system_identifier", "StringSystemIdentifier, IntSystemIdentifier"),
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
        lines.append("    # URIs exposed by the bridge")
        for _, data in self._definitions["mappings"]["bridge"].items():
            lines.append(f"    {data['uri']['var_name']} = \"{data['uri']['value']}\"  # {data['title']}")

        lines.append("")
        lines.append("    # URIs exposed by the client")
        for _, data in self._definitions["mappings"]["client"].items():
            if "bridge" in data["sender"]:
                lines.append(f"    {data['uri']['var_name']} = \"{data['uri']['value']}\"  # {data['title']}")

        lines.append("")
        lines.append("")

        lines.append(f"class {PY_CLASSNAME_ACCESS_LEVEL}(IntSystemIdentifier):")
        lines.append(f"    \"\"\"Container for all API access levels\"\"\"")
        lines.append("")

        for mapping, data in self._definitions["access_level"].items():
            lines.append(f"    {data['var_name']} = {data['id']}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append(f"class {PY_CLASSNAME_ACCESS_LEVEL_MAPPING}:")
        lines.append(f"    \"\"\"Container for all API access levels\"\"\"")
        lines.append("")

        mappings = {}
        for key, data in self._definitions["access_level"].items():
            mappings[key] = []
        for mapping, data in self._definitions["mappings"]["bridge"].items():
            for access_level in data["access_level"]:
                try:
                    mappings[access_level].append(data["uri"]["var_name"])
                except KeyError:
                    raise Exception(f"Invalid access_level {access_level} in mapping {mapping}")
        # lines.append(str(mappings))

        lines.append("    mapping = {")
        for index, (key, data) in enumerate(mappings.items()):
            map_list = [f'{PY_CLASSNAME_URIS}.{x}' for x in data]
            line_end = "," if index < len(mappings)-1 else ""
            lines.append(f"        {PY_CLASSNAME_ACCESS_LEVEL}.{key}: [{', '.join(map_list)}]{line_end}")

        lines.append("    }")

        lines.append("")

        lines.append("    @classmethod")
        lines.append(f"    def get_mapping(cls, access_level: {PY_CLASSNAME_ACCESS_LEVEL}) -> list[{PY_CLASSNAME_URIS}]:")
        lines.append("        return cls.mapping[access_level]")


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

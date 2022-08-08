from typing import Optional

from exporters.constants_export import ConstantsExporterPython
from exporters.def_code_type_names import PY_CLASSNAME_API_DEFINITION_CONTAINER, PY_CLASSNAME_ACCESS_TYPE, \
    PY_CLASSNAME_ACCESS_TYPE_SUPER, PY_CLASSNAME_URIS_SUPER, PY_CLASSNAME_ENDPOINT_TYPE_SUPER, PY_VARNAME_API_VERSION, \
    PY_CLASSNAME_ACCESS_LEVEL, PY_CLASSNAME_ENDPOINT_TYPE, PY_CLASSNAME_URIS
from exporters.def_docstrings import DOCSTR_API_CONSTANTS


class ConstantExporterApiPython(ConstantsExporterPython):

    def _export_definition(self, data: dict, access_levels_data: dict, linebreak: bool, bridge_is_requester: bool,
                           category: Optional[str]) -> list[str]:
        if "access_level" in data:
            access_level_buffer = [access_levels_data[x]["var_name"] for x in access_levels_data if
                                   x in data["access_level"]]
            access_levels = f"[{', '.join([f'{PY_CLASSNAME_ACCESS_LEVEL}.{x}' for x in access_level_buffer])}]"
        else:
            access_levels = "[]"

        requires_response = data["response"]["schema"] is not None

        if linebreak:
            indent = "\n" + " " * (len(data['uri']['var_name']) + len(PY_CLASSNAME_API_DEFINITION_CONTAINER) + 8)
        else:
            indent = " "

        cat_str = "None"
        if category is not None:
            cat_str = PY_CLASSNAME_ENDPOINT_TYPE + "." + category

        lines = [""]
        uri = data['uri']['value']
        access_type = f"{PY_CLASSNAME_ACCESS_TYPE}.{data['access_type']}" if "access_type" in data else "None"

        lines.append(f"    # {data['title']}")
        lines.append(
            f"    {data['uri']['var_name']} = {PY_CLASSNAME_API_DEFINITION_CONTAINER}(\"{uri}\",{indent}{access_levels},{indent}{cat_str},{indent}{access_type},{indent}{bridge_is_requester},{indent}{requires_response})")
        return lines

    def export(self, filename: str):
        lines = self._generate_header(DOCSTR_API_CONSTANTS, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        lines.append("import enum")
        lines.append("")

        for x in self._generate_imports([("utils.api_endpoint_definition",
                                          f"{PY_CLASSNAME_API_DEFINITION_CONTAINER}, {PY_CLASSNAME_ACCESS_TYPE}, {PY_CLASSNAME_ACCESS_TYPE_SUPER}, {PY_CLASSNAME_URIS_SUPER}, {PY_CLASSNAME_ENDPOINT_TYPE_SUPER}"),
                                         ("utils.software_version", "SoftwareVersion")]):
            lines.append(x)

        lines.append("")
        lines.append("")

        lines.append("# API Version")

        lines.append(
            f"{PY_VARNAME_API_VERSION} = SoftwareVersion({self._api_version.major}, {self._api_version.minor}, {self._api_version.bugfix})")

        lines.append("")
        lines.append("")

        lines.append(f"class {PY_CLASSNAME_ACCESS_LEVEL}({PY_CLASSNAME_ACCESS_TYPE_SUPER}, enum.IntEnum):")
        lines.append(f"    \"\"\"Container for all API access levels\"\"\"")
        lines.append("")

        access_level_data = self._api_access_level_def["items"]
        for mapping, data in access_level_data.items():
            lines.append(f"    {data['var_name']} = {data['id']}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append(f"class {PY_CLASSNAME_ENDPOINT_TYPE}({PY_CLASSNAME_ENDPOINT_TYPE_SUPER}, enum.IntEnum):")
        lines.append(f"    \"\"\"Container for all API endpoint types\"\"\"")
        lines.append("")

        for index, (endpoint_id, data) in enumerate(self._api_endpoint_def["items"]["bridge"].items()):
            lines.append(f"    {endpoint_id.capitalize()} = {index}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append(f"class {PY_CLASSNAME_URIS}({PY_CLASSNAME_URIS_SUPER}):")
        lines.append(f"    \"\"\"Container for all API URIs\"\"\"")
        lines.append("")
        lines.append("    # URIs exposed by the bridge")
        for category, definitions in self._api_endpoint_def["items"]["bridge"].items():
            cat_value = category.capitalize()
            for _, data in definitions["endpoints"].items():
                lines += self._export_definition(data, access_level_data, True, False, cat_value)

        lines.append("")
        lines.append("    # URIs exposed by the client")
        for _, data in self._api_endpoint_def["items"]["client"].items():
            if "bridge" in data["sender"]:
                lines += self._export_definition(data, access_level_data, False, True, None)

        with open(filename, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

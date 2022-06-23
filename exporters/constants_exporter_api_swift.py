from system.exporters.constants_export import ConstantsExporterSwift
from system.exporters.def_code_type_names import SWIFT_VARNAME_API_VERSION, SWIFT_CLASSNAME_API_VERSION, \
    SWIFT_CLASSNAME_URIS
from system.exporters.def_docstrings import DOCSTR_API_CONSTANTS


class ConstantExporterApiSwift(ConstantsExporterSwift):

    def export(self, filename: str):
        # Filter data to only export api constants relevant to the web interface
        filtered_data = []
        for category, cat_data in self._api_endpoint_def["items"]["bridge"].items():
            for key, data in cat_data["endpoints"].items():
                if "web_application" in data["sender"]:
                    data["receiver"] = "bridge"
                    filtered_data.append(data)

        lines = self._generate_header(DOCSTR_API_CONSTANTS, '/'.join(__file__.split('/')[-1:]))

        lines.append("")
        lines.append("")

        lines.append(
            f"let {SWIFT_VARNAME_API_VERSION} = {SWIFT_CLASSNAME_API_VERSION}(major={self._api_version.major}, minor={self._api_version.minor}, bugfix={self._api_version.bugfix})")

        lines.append("")
        lines.append("")

        lines.append(f"enum {SWIFT_CLASSNAME_URIS} : String " + "{")

        for data in filtered_data:
            lines.append(f"    case {data['uri']['var_name']} = \"{data['uri']['value']}\"   // {data['title']}")

        lines.append("}")

        with open(filename, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

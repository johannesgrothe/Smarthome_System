from system.exporters.constants_export import ConstantsExporterJavaScript
from system.exporters.def_code_type_names import JS_CLASSNAME_API
from system.exporters.def_docstrings import DOCSTR_API_CONSTANTS
from system.utils.js_file import *


class ConstantExporterApiJavaScript(ConstantsExporterJavaScript):

    def export(self, filename: str):
        filtered_data = []
        for category, cat_data in self._api_endpoint_def["items"]["bridge"].items():
            for key, data in cat_data["endpoints"].items():
                if "web_application" in data["sender"]:
                    data["receiver"] = "bridge"
                    filtered_data.append(data)

        file = JSFile()

        self._add_header(DOCSTR_API_CONSTANTS, '/'.join(__file__.split('/')[-1:]), file)

        api_constants_class = JSConstantsClass(JS_CLASSNAME_API,
                                               "Class for all API constants and definitions")

        api_constants_class.add(JSBlankLine())

        api_constants_class.add(JSComment("API Version"))

        api_constants_class.add(JSVariable("static", "version_major", self._api_version.major))
        api_constants_class.add(JSVariable("static", "version_minor", self._api_version.minor))
        api_constants_class.add(JSVariable("static", "version_bugfix", self._api_version.bugfix))

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

        file.save(filename)

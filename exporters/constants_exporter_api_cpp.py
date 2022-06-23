from system.exporters.constants_export import ConstantsExporterCpp
from system.exporters.def_code_type_names import CPP_NAMESPACE_API_DOCS, CPP_NAMESPACE_API_VERSION, \
    CPP_NAMESPACE_API_URIS
from system.exporters.def_docstrings import DOCSTR_API_CONSTANTS
from system.utils.cpp_file import *
from system.utils.software_version import SoftwareVersion


class ConstantExporterApiCpp(ConstantsExporterCpp):

    def export(self, filename: str):
        # Filter data to only export api constants relevant to the client
        filtered_data = []
        for category, cat_data in self._api_endpoint_def["items"]["bridge"].items():
            for key, data in cat_data["endpoints"].items():
                if "client" in data["sender"]:
                    data["receiver"] = "bridge"
                    filtered_data.append(data)
        for key, data in self._api_endpoint_def["items"]["client"].items():
            data["receiver"] = "client"
            filtered_data.append(data)

        file = CppFile()

        self._add_header(DOCSTR_API_CONSTANTS, '/'.join(__file__.split('/')[-1:]), file)

        file.add(CppImport("string", in_package=False))
        file.add(CppImport("cstdint", in_package=False))

        package_namespace = CppNamespace(CPP_NAMESPACE_API_DOCS,
                                         "Namespace for all api constants and definitions")

        version_namespace = CppNamespace(CPP_NAMESPACE_API_VERSION,
                                         "API Version")
        version_namespace.add(CppVariable("constexpr uint8_t", "major", self._api_version.major))
        version_namespace.add(CppVariable("constexpr uint8_t", "minor", self._api_version.minor))
        version_namespace.add(CppVariable("constexpr uint8_t", "bugfix", self._api_version.bugfix))

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

        file.save(filename)

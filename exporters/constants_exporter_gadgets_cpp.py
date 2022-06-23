from system.exporters.constants_export import ConstantsExporterCpp
from system.exporters.def_code_type_names import *
from system.exporters.def_docstrings import DOCSTR_GADGET_CONSTANTS
from system.utils.cpp_file import *


class ConstantExporterGadgetsCpp(ConstantsExporterCpp):

    def export(self, filename: str):
        file = CppFile()

        self._add_header(DOCSTR_GADGET_CONSTANTS, '/'.join(__file__.split('/')[-1:]), file)

        file.add(CppImport("cstdint", in_package=False))

        package_namespace = CppNamespace(CPP_NAMESPACE_GADGET_DOCS,
                                         "Namespace for all gadget and characteristic definitions")

        package_namespace.add(CppBlankLine())
        package_namespace.add(CppComment("Count of the different gadget identifiers"))
        package_namespace.add(CppVariable("constexpr uint8_t",
                                          "GadgetIdentifierCount",
                                          len(self._gadgets_remote['items'])))

        gadget_enum = CppEnumClass("GadgetIdentifier",
                                   self._gadgets_remote['description'])

        for key, data in self._gadgets_remote["items"].items():
            gadget_enum.add_element(key, data['enum_value'], data['name'])

        package_namespace.add(gadget_enum)

        file.add(package_namespace)

        file.save(filename)

"""Module for the gadget constants exporter"""
from exporters.constants_exporter import ConstantsExporter
from exporters.script_params import CPP_NAMESPACE_GADGET_DOCS
from utils.cpp_file import *

_export_file_docstring = "Collection of constants for all gadgets and characteristics"


class GadgetConstantsExporter(ConstantsExporter):
    """Class that handles the gadget doc exporting process"""

    _definitions: dict

    def __init__(self, definitions: str):
        super().__init__(definitions)

    def export_python(self, out_file: str):
        characteristics_data = self._definitions["characteristic_definitions"]
        client_gadget_data = self._definitions["gadget_definitions"]["client_gadgets"]
        bridge_gadget_data = self._definitions["gadget_definitions"]["bridge_gadgets"]

        lines = self._generate_python_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        for x in self._generate_python_imports([("utils.system_identifier", "IntSystemIdentifier")]):
            lines.append(x)

        lines.append("")
        lines.append("")

        lines.append("class CharacteristicIdentifier(IntSystemIdentifier):")
        lines.append(f"    \"\"\"{characteristics_data['description']}\"\"\"")
        lines.append("")

        for key, data in characteristics_data["items"].items():
            lines.append(f"    {key} = {data['enum_value']}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append("class GadgetIdentifier(IntSystemIdentifier):")
        lines.append(f"    \"\"\"{client_gadget_data['description']}\"\"\"")
        lines.append("")

        for key, data in client_gadget_data["items"].items():
            lines.append(f"    {key} = {data['enum_value']}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append("class BridgeGadgetIdentifier(IntSystemIdentifier):")
        lines.append(f"    \"\"\"{bridge_gadget_data['description']}\"\"\"")
        lines.append("")

        for key, data in bridge_gadget_data["items"].items():
            lines.append(f"    {key} = {data['enum_value']}  # {data['name']}")

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

    def export_cpp(self, out_file: str):
        characteristics_data = self._definitions["characteristic_definitions"]
        client_gadget_data = self._definitions["gadget_definitions"]["client_gadgets"]

        file = CppFile()

        self._add_cpp_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]), file)

        package_namespace = CppNamespace(CPP_NAMESPACE_GADGET_DOCS,
                                         "Namespace for all gadget and characteristic definitions")

        package_namespace.add(CppBlankLine())
        package_namespace.add(CppComment("Count of the different gadget identifiers"))
        package_namespace.add(CppVariable("constexpr uint8_t",
                                          "GadgetIdentifierCount",
                                          len(client_gadget_data['items'])))

        package_namespace.add(CppBlankLine())
        package_namespace.add(CppComment("Count of the different characteristic identifiers"))
        package_namespace.add(CppVariable("constexpr uint8_t",
                                          "CharacteristicIdentifierCount",
                                          len(characteristics_data['items'])))

        gadget_enum = CppEnumClass("GadgetIdentifier",
                                   client_gadget_data['description'])

        for key, data in client_gadget_data["items"].items():
            gadget_enum.add_element(key, data['enum_value'], data['name'])

        package_namespace.add(gadget_enum)

        gadget_enum = CppEnumClass("CharacteristicIdentifier",
                                   characteristics_data['description'])

        for key, data in characteristics_data["items"].items():
            gadget_enum.add_element(key, data['enum_value'], data['name'])

        package_namespace.add(gadget_enum)

        file.add(package_namespace)

        file.save(out_file)

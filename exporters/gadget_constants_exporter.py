"""Module for the gadget constants exporter"""
from exporters.constants_exporter import ConstantsExporter
from exporters.script_params import CPP_NAMESPACE_GADGET_DOCS, JS_CLASSNAME_GADGET_SPECS
from utils.cpp_file import *
from utils.js_file import *

_export_file_docstring = "Collection of constants for all gadgets and characteristics"


class GadgetConstantsExporter(ConstantsExporter):
    """Class that handles the gadget doc exporting process"""

    _definitions: dict

    def __init__(self, definitions: str):
        super().__init__(definitions)

    def export_python(self, out_file: str):
        client_gadget_data = self._definitions["gadget_definitions"]["client_gadgets"]
        bridge_gadget_data = self._definitions["gadget_definitions"]["bridge_gadgets"]
        gadget_class_data = self._definitions["gadget_classes"]

        lines = self._generate_python_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        lines.append("import enum")

        lines.append("")
        lines.append("")

        lines.append("class GadgetIdentifier(enum.IntEnum):")
        lines.append(f"    \"\"\"{client_gadget_data['description']}\"\"\"")
        lines.append("")

        for key, data in client_gadget_data["items"].items():
            lines.append(f"    {key} = {data['enum_value']}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append("class BridgeGadgetIdentifier(enum.IntEnum):")
        lines.append(f"    \"\"\"{bridge_gadget_data['description']}\"\"\"")
        lines.append("")

        for key, data in bridge_gadget_data["items"].items():
            lines.append(f"    {key} = {data['enum_value']}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append("class GadgetClass(enum.IntEnum):")
        lines.append(f"    \"\"\"{gadget_class_data['description']}\"\"\"")
        lines.append("")

        for key, data in gadget_class_data["items"].items():
            lines.append(f"    {key} = {data['enum_value']}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append("GadgetClassMapping = {")

        for i, (key, data) in enumerate(gadget_class_data["items"].items()):
            class_val = data['enum_value']
            local_gadgets = ["BridgeGadgetIdentifier." + key for key, data in bridge_gadget_data["items"].items() if
                             data['class'] == class_val]
            remote_gadgets = ["GadgetIdentifier." + key for key, data in client_gadget_data["items"].items() if
                              data['class'] == class_val]
            sep = "," if i < len(gadget_class_data["items"]) - 1 else ""
            lines.append(f"    GadgetClass.{key}: [{', '.join(local_gadgets + remote_gadgets)}]{sep}")
        lines.append("}")

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

    def export_cpp(self, out_file: str):
        # characteristics_data = self._definitions["characteristic_definitions"]
        client_gadget_data = self._definitions["gadget_definitions"]["client_gadgets"]

        file = CppFile()

        self._add_cpp_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]), file)

        file.add(CppImport("cstdint", in_package=False))

        package_namespace = CppNamespace(CPP_NAMESPACE_GADGET_DOCS,
                                         "Namespace for all gadget and characteristic definitions")

        package_namespace.add(CppBlankLine())
        package_namespace.add(CppComment("Count of the different gadget identifiers"))
        package_namespace.add(CppVariable("constexpr uint8_t",
                                          "GadgetIdentifierCount",
                                          len(client_gadget_data['items'])))

        # package_namespace.add(CppBlankLine())
        # package_namespace.add(CppComment("Count of the different characteristic identifiers"))
        # package_namespace.add(CppVariable("constexpr uint8_t",
        #                                   "CharacteristicIdentifierCount",
        #                                   len(characteristics_data['items'])))

        gadget_enum = CppEnumClass("GadgetIdentifier",
                                   client_gadget_data['description'])

        for key, data in client_gadget_data["items"].items():
            gadget_enum.add_element(key, data['enum_value'], data['name'])

        package_namespace.add(gadget_enum)

        # characteristic_enum = CppEnumClass("CharacteristicIdentifier",
        #                                    characteristics_data['description'])
        #
        # for key, data in characteristics_data["items"].items():
        #     characteristic_enum.add_element(key, data['enum_value'], data['name'])

        # package_namespace.add(characteristic_enum)

        file.add(package_namespace)

        file.save(out_file)

    def export_js(self, out_file: str):
        # characteristics_data = self._definitions["characteristic_definitions"]
        client_gadget_data = self._definitions["gadget_definitions"]["client_gadgets"]

        file = JSFile()

        gadget_definitions_class = JSConstantsClass(JS_CLASSNAME_GADGET_SPECS,
                                                    "CLass for all gadget and characteristic definitions")

        gadget_definitions_class.add(JSBlankLine())
        gadget_definitions_class.add(JSComment("Count of the different gadget identifiers"))
        gadget_definitions_class.add(JSVariable("static",
                                                "GadgetIdentifierCount",
                                                len(client_gadget_data['items'])))

        # gadget_definitions_class.add(JSBlankLine())
        # gadget_definitions_class.add(JSComment("Count of the different characteristic identifiers"))
        # gadget_definitions_class.add(JSVariable("static",
        #                                         "CharacteristicIdentifierCount",
        #                                         len(characteristics_data['items'])))

        gadget_definitions_class.add(JSBlankLine())
        gadget_definitions_class.add(JSComment("Gadget Identifier"))
        for index, (key, data) in enumerate(client_gadget_data["items"].items()):
            gadget_definitions_class.add(JSVariable("static", "gadget_" + key, data['enum_value'], data['name']))

        # gadget_definitions_class.add(JSBlankLine())
        # gadget_definitions_class.add(JSComment("Characteristic Identifier"))
        # for index, (key, data) in enumerate(characteristics_data["items"].items()):
        #     gadget_definitions_class.add(
        #         JSVariable("static", "characteristic_" + key, data['enum_value'], data['name']))

        file.add(gadget_definitions_class)

        file.save(out_file)

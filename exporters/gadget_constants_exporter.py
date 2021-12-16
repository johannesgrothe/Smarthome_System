"""Module for the gadget constants exporter"""
from exporters.constants_exporter import ConstantsExporter

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

    @staticmethod
    def export_enum_class_items(enum_data: dict, lines: list[str]):
        for index, (key, data) in enumerate(enum_data.items()):
            if index < len(enum_data) - 1:
                lines.append(f"        {key} = {data['enum_value']},  // {data['name']}")
            else:
                lines.append(f"        {key} = {data['enum_value']}  // {data['name']}")
        lines.append("    }")

    def export_cpp(self, out_file: str):
        characteristics_data = self._definitions["characteristic_definitions"]
        client_gadget_data = self._definitions["gadget_definitions"]["client_gadgets"]

        lines = self._generate_cpp_header(_export_file_docstring, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        lines.append("// Namespace for all gadget and characteristic definitions")
        lines.append("namespace gadget_definitions {")

        lines.append("")
        lines.append("    // Count of the different gadget identifiers")
        lines.append(f"    constexpr uint8_t GadgetIdentifierCount = {len(client_gadget_data['items'])};")
        lines.append("")
        lines.append("    // Count of the different characteristic identifiers")
        lines.append(f"    constexpr uint8_t CharacteristicIdentifierCount = {len(characteristics_data['items'])};")

        lines.append("")
        lines.append(f"    // {client_gadget_data['description']}")
        lines.append("    enum class GadgetIdentifier {")
        self.export_enum_class_items(client_gadget_data["items"], lines)

        lines.append("")
        lines.append(f"    // {characteristics_data['description']}")
        lines.append("    enum class CharacteristicIdentifier {")
        self.export_enum_class_items(characteristics_data["items"], lines)

        lines.append("}")

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

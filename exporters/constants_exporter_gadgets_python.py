from exporters.constants_export import ConstantsExporterPython
from exporters.def_code_type_names import *
from exporters.def_docstrings import DOCSTR_GADGET_CONSTANTS


class ConstantExporterGadgetsPython(ConstantsExporterPython):

    def export(self, filename: str):
        lines = self._generate_header(DOCSTR_GADGET_CONSTANTS, '/'.join(__file__.split('/')[-1:]))

        lines.append("")

        lines.append("import enum")

        lines.append("")
        lines.append("")

        lines.append(f"class {PY_CLASSNAME_GADGET_IDENTIFIER_REMOTE}(enum.IntEnum):")
        lines.append(f"    \"\"\"{self._gadgets_remote['description']}\"\"\"")
        lines.append("")

        for key, data in self._gadgets_remote["items"].items():
            lines.append(f"    {key} = {data['enum_value']}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append(f"class {PY_CLASSNAME_GADGET_IDENTIFIER_LOCAL}(enum.IntEnum):")
        lines.append(f"    \"\"\"{self._gadgets_local['description']}\"\"\"")
        lines.append("")

        for key, data in self._gadgets_local["items"].items():
            lines.append(f"    {key} = {data['enum_value']}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append(f"class {PY_CLASSNAME_GADGET_CLASS}(enum.IntEnum):")
        lines.append(f"    \"\"\"{self._gadget_class_def['description']}\"\"\"")
        lines.append("")

        for key, data in self._gadget_class_def["items"].items():
            lines.append(f"    {key} = {data['enum_value']}  # {data['name']}")

        lines.append("")
        lines.append("")

        lines.append(f"{PY_VARNAME_GADGET_CLASS_MAPPING} = " + "{")

        for i, (key, data) in enumerate(self._gadget_class_def["items"].items()):
            class_val = data['enum_value']
            local_gadgets = [f"{PY_CLASSNAME_GADGET_IDENTIFIER_LOCAL}." + key for key, data in
                             self._gadgets_local["items"].items() if
                             data['class'] == class_val]
            remote_gadgets = [f"{PY_CLASSNAME_GADGET_IDENTIFIER_REMOTE}." + key for key, data in
                              self._gadgets_remote["items"].items() if
                              data['class'] == class_val]
            sep = "," if i < len(self._gadget_class_def["items"]) - 1 else ""
            lines.append(f"    GadgetClass.{key}: [{', '.join(local_gadgets + remote_gadgets)}]{sep}")
        lines.append("}")

        with open(filename, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

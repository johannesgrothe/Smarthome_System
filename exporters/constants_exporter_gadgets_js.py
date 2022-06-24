from exporters.constants_export import ConstantsExporterJavaScript
from exporters.def_code_type_names import *
from exporters.def_docstrings import DOCSTR_GADGET_CONSTANTS
from utils.js_file import *


class ConstantExporterGadgetsJavaScript(ConstantsExporterJavaScript):

    def export(self, filename: str):
        file = JSFile()

        self._add_header(DOCSTR_GADGET_CONSTANTS, '/'.join(__file__.split('/')[-1:]), file)

        gadget_definitions_class = JSConstantsClass(JS_CLASSNAME_GADGET_SPECS,
                                                    "CLass for all gadget and characteristic definitions")

        gadget_definitions_class.add(JSBlankLine())
        gadget_definitions_class.add(JSComment("Count of the different gadget identifiers"))
        gadget_definitions_class.add(JSVariable("static",
                                                "GadgetIdentifierCount",
                                                len(self._gadgets_remote['items'])))

        gadget_definitions_class.add(JSBlankLine())
        gadget_definitions_class.add(JSComment("Gadget Identifier"))
        for index, (key, data) in enumerate(self._gadgets_remote["items"].items()):
            gadget_definitions_class.add(JSVariable("static", "gadget_" + key, data['enum_value'], data['name']))

        file.add(gadget_definitions_class)

        file.save(filename)

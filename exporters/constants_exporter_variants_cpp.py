from exporters.constants_export import ConstantsExporterCpp
from exporters.def_docstrings import DOCSTR_VARIANT_CONSTANTS
from utils.cpp_file import *


class ConstantExporterVariantsCpp(ConstantsExporterCpp):

    def export(self, filename: str):
        file = CppFile()

        self._add_header(DOCSTR_VARIANT_CONSTANTS, '/'.join(__file__.split('/')[-1:]), file)

        hw_variants_enum = CppEnumClass("HwVariant",
                                        self._hw_variant_def["description"])

        for i, variant_data in enumerate(self._hw_variant_def["variants"]):
            hw_variants_enum.add_element(variant_data["name"], i + 1, variant_data["description"])

        file.add(hw_variants_enum)

        sw_variants_enum = CppEnumClass("SwVariant",
                                        self._sw_variant_def["description"])

        for i, variant_data in enumerate(self._sw_variant_def["variants"]):
            sw_variants_enum.add_element(variant_data["name"], i + 1, variant_data["description"])

        file.add(sw_variants_enum)

        file.save(filename)

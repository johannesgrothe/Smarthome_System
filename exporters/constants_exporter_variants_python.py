from exporters.constants_export import ConstantsExporterPythonFile
from exporters.def_docstrings import DOCSTR_VARIANT_CONSTANTS
from utils.cpp_file import *
from utils.py_file import PythonFile, PythonEnum, PythonPackageImport


class ConstantExporterVariantsPython(ConstantsExporterPythonFile):

    def export(self, filename: str):
        file = PythonFile()

        self._add_header(DOCSTR_VARIANT_CONSTANTS, '/'.join(__file__.split('/')[-1:]), file)

        file.add(PythonPackageImport("enum"))

        hw_variants_enum = PythonEnum("HwVariant",
                                      self._hw_variant_def["description"])

        for i, variant_data in enumerate(self._hw_variant_def["variants"]):
            hw_variants_enum.add_element(variant_data["name"], i + 1, variant_data["description"])

        file.add(hw_variants_enum)

        sw_variants_enum = PythonEnum("SwVariant",
                                      self._sw_variant_def["description"])

        for i, variant_data in enumerate(self._sw_variant_def["variants"]):
            sw_variants_enum.add_element(variant_data["name"], i + 1, variant_data["description"])

        file.add(sw_variants_enum)

        file.save(filename)

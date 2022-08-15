from exporters.constants_export import ConstantsExporterSwift
from exporters.def_docstrings import DOCSTR_GADGET_CONSTANTS


class ConstantExporterGadgetsSwift(ConstantsExporterSwift):

    def export(self, filename: str):
        lines = self._generate_header(DOCSTR_GADGET_CONSTANTS, '/'.join(__file__.split('/')[-1:]))
        with open(filename, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

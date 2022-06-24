import os

import pytest

from exporters.def_filenames import *

from exporters.constants_exporter_api_cpp import ConstantExporterApiCpp
from exporters.constants_exporter_api_python import ConstantExporterApiPython
from exporters.constants_exporter_api_js import ConstantExporterApiJavaScript
from exporters.constants_exporter_api_swift import ConstantExporterApiSwift
from exporters.constants_exporter_gadgets_cpp import ConstantExporterGadgetsCpp
from exporters.constants_exporter_gadgets_js import ConstantExporterGadgetsJavaScript
from exporters.constants_exporter_gadgets_python import ConstantExporterGadgetsPython
from exporters.constants_exporter_gadgets_swift import ConstantExporterGadgetsSwift


def compare_files(old: str, new: str):
    print(f"Checking '{old}' against '{new}'")

    with open(old, "r") as file_h:
        check_lines = file_h.readlines()

    with open(new, "r") as file_h:
        exported_lines = file_h.readlines()

    assert len(check_lines) == len(exported_lines)

    for check_line, exported_line in zip(check_lines, exported_lines):
        assert check_line == exported_line


@pytest.mark.pr_only
def test_api_constants(assert_temp: str):
    new_file = os.path.join(assert_temp, FILE_API_CONSTANTS_PY)
    ConstantExporterApiPython().export(new_file)
    compare_files(FILE_API_CONSTANTS_PY, new_file)

    new_file = os.path.join(assert_temp, FILE_API_CONSTANTS_JS)
    ConstantExporterApiJavaScript().export(new_file)
    compare_files(FILE_API_CONSTANTS_JS, new_file)

    new_file = os.path.join(assert_temp, FILE_API_CONSTANTS_CPP)
    ConstantExporterApiCpp().export(new_file)
    compare_files(FILE_API_CONSTANTS_CPP, new_file)

    new_file = os.path.join(assert_temp, FILE_API_CONSTANTS_SWIFT)
    ConstantExporterApiSwift().export(new_file)
    compare_files(FILE_API_CONSTANTS_SWIFT, new_file)


@pytest.mark.pr_only
def test_gadget_constants(assert_temp: str):
    new_file = os.path.join(assert_temp, FILE_GADGET_CONSTANTS_PY)
    ConstantExporterGadgetsPython().export(new_file)
    compare_files(FILE_GADGET_CONSTANTS_PY, new_file)

    new_file = os.path.join(assert_temp, FILE_GADGET_CONSTANTS_CPP)
    ConstantExporterGadgetsCpp().export(os.path.join(new_file))
    compare_files(FILE_GADGET_CONSTANTS_CPP, new_file)

    new_file = os.path.join(assert_temp, FILE_GADGET_CONSTANTS_JS)
    ConstantExporterGadgetsJavaScript().export(os.path.join(new_file))
    compare_files(FILE_GADGET_CONSTANTS_JS, new_file)

    new_file = os.path.join(assert_temp, FILE_GADGET_CONSTANTS_SWIFT)
    ConstantExporterGadgetsSwift().export(os.path.join(new_file))
    compare_files(FILE_GADGET_CONSTANTS_SWIFT, new_file)

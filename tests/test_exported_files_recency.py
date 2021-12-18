import pytest

from exporters.api_constants_exporter import ApiConstantsExporter
from exporters.gadget_constants_exporter import GadgetConstantsExporter
from exporters.script_params import *


@pytest.fixture
def exported_temp_files(temp_exists):
    print("Creating temporary files")
    path_temp_api_export = os.path.join(PATH_TEMP_DIR, PATH_FILE_API_CONSTANTS)
    temp_files = [f"{path_temp_api_export}.py", f"{path_temp_api_export}.h"]

    path_temp_gadgets_export = os.path.join(PATH_TEMP_DIR, PATH_FILE_GADGET_CONSTANTS)
    temp_files += [f"{path_temp_gadgets_export}.py", f"{path_temp_gadgets_export}.h"]

    exporter = ApiConstantsExporter(PATH_API_SPECS)
    exporter.export_python(f"{path_temp_api_export}.py")
    exporter.export_cpp(f"{path_temp_api_export}.h")

    exporter = GadgetConstantsExporter(PATH_GADGET_SPECS)
    exporter.export_python(f"{path_temp_gadgets_export}.py")
    exporter.export_cpp(f"{path_temp_gadgets_export}.h")

    yield temp_files


@pytest.mark.pr_only
def test_constant_files(exported_temp_files):
    for file in exported_temp_files:
        original_filename = file.split(os.sep)[-1]
        print(f"Checking '{file}' against '{original_filename}'")

        with open(file, "r") as file_h:
            check_lines = file_h.readlines()

        with open(original_filename, "r") as file_h:
            exported_lines = file_h.readlines()

        assert len(check_lines) == len(exported_lines)

        for check_line, exported_line in zip(check_lines, exported_lines):
            assert check_line == exported_line

import pytest

from exporters.api_constants_exporter import ApiConstantsExporter
from exporters.gadget_constants_exporter import GadgetConstantsExporter
from exporters.script_params import *
from exporters.temp_dir_manager import TempDirManager


@pytest.fixture
def temp_exists():
    print("Creating temp dir")
    TempDirManager(PATH_TEMP_DIR).assert_temp()
    yield None
    print("Removing temporary files")
    TempDirManager(PATH_TEMP_DIR).clean_temp()


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


def test_python_file_integrity():
    print("Importing python files to check integrity")
    import api_definitions
    import gadget_definitions


def test_cpp_file_integrity(temp_exists):
    print("Compiling c++ files to check integrity")
    import os
    return_code = os.system("g++ -o temp/test tests/cpp_compile_test.cpp -std=c++11")
    assert return_code == 0
    print("Executing c++ files to check included tests")
    return_code = os.system("./temp/test")
    assert return_code == 0

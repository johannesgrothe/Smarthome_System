import os
import sys
import json
import jsonschema
import pytest

from api_docs.export_api_constants import ApiConstantsExporter
from api_docs.script_params import *


def remove_first_dir(path: str) -> str:
    return os.path.join(*(path.split(os.path.sep)[1:]))


@pytest.fixture
def temp_exists():
    temp_path = remove_first_dir(PATH_TEMP_DIR)
    if not os.path.isdir(temp_path):
        os.mkdir(temp_path)


@pytest.fixture
def exported_temp_files(temp_exists):
    print("Creating temporary files")
    temp_path = remove_first_dir(PATH_TEMP_DIR)
    path_temp_export = os.path.join(temp_path, remove_first_dir(PATH_FILE_CONSTANTS))
    temp_files = [f"{path_temp_export}.py", f"{path_temp_export}.h"]

    exporter = ApiConstantsExporter(os.path.join("api_docs", PATH_API_SPECS))
    exporter.export_api_constants_python(f"{path_temp_export}.py")
    exporter.export_api_constants_cpp(f"{path_temp_export}.h")
    yield temp_files
    print("Removing temporary files")
    for file in temp_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


@pytest.mark.pr_only
def test_constant_files(exported_temp_files):
    for file in exported_temp_files:
        original_filename = remove_first_dir(PATH_FILE_CONSTANTS) + "." + file.split(".")[-1]
        print(f"Checking '{file}' against '{original_filename}'")

        with open(file, "r") as file_h:
            check_lines = file_h.readlines()

        with open(original_filename, "r") as file_h:
            exported_lines = file_h.readlines()

        assert len(check_lines) == len(exported_lines)

        for check_line, exported_line in zip(check_lines, exported_lines):
            assert check_line == exported_line

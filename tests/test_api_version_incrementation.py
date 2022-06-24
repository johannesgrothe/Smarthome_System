import os
import json
import shutil
import pytest

from utils.software_version import SoftwareVersion
from utils.schema_loader import SchemaLoader


def load_api_version(src_file: str) -> SoftwareVersion:
    try:
        with open(src_file, "r") as file_p:
            file_data = json.load(file_p)
            return SoftwareVersion.from_string(file_data["version"])
    except KeyError:
        return SoftwareVersion(0, 0, 1)


def compare_schemas(current: dict, old: dict) -> bool:
    """Returns true if schemas are functionally the same"""
    return current == old


def compare_api_definitions(current_file: str, last_file: str, current_schema_path: str, old_schema_path: str) -> bool:
    """returns true if api definitions are functionally the same"""
    with open(current_file, "r") as file_p:
        current_data = json.load(file_p)
    with open(last_file, "r") as file_p:
        last_data = json.load(file_p)

    try:
        if current_data["mappings"].keys() != last_data["mappings"].keys():
            return True

        current_schemas = SchemaLoader(current_schema_path).load_schemas()
        old_schemas = SchemaLoader(old_schema_path).load_schemas()

        for mapping in current_data["mappings"]:
            buf_curr = current_data["mappings"][mapping]
            buf_last = last_data["mappings"][mapping]

            if buf_curr.keys() != buf_last.keys():
                return False

            if buf_curr["uri"]["value"] != buf_last["uri"]["value"]:
                return False

            try:
                if not compare_schemas(current_schemas[buf_curr["request"]["schema"].strip(".json")],
                                       old_schemas[buf_last["request"]["schema"].strip(".json")]):
                    return False
            except AttributeError:
                pass

            try:
                if not compare_schemas(current_schemas[buf_curr["response"]["schema"].strip(".json")],
                                       old_schemas[buf_last["response"]["schema"].strip(".json")]):
                    return False
            except AttributeError:
                pass

    except KeyError:
        return False

    return True


@pytest.mark.pr_only
def test_api_version_incrementation(assert_temp):
    current_version = load_api_version(os.path.join("api_docs", "api_specs.json"))
    source_dir = os.path.join(os.getcwd(), "temp", "repo", ".git")
    base_dir = os.path.join(os.getcwd(), ".git")
    print(f"Copying '{base_dir}' to '{source_dir}'")

    shutil.copytree(base_dir, source_dir)
    return_code = os.system("cd temp/repo && git reset --hard && git checkout origin/master")
    assert return_code == 0
    last_version = load_api_version(os.path.join("temp", "repo", "api_docs", "api_specs.json"))
    print(f"API Versions: {last_version} (master); {current_version} (current branch)")
    assert last_version == current_version or current_version.follows(last_version)
    if not compare_api_definitions(os.path.join(os.getcwd(), "api_docs", "api_specs.json"),
                                   os.path.join(os.getcwd(), "temp", "repo", "api_docs", "api_specs.json"),
                                   os.path.join(os.getcwd(), "json_schemas"),
                                   os.path.join(os.getcwd(), "temp", "repo", "json_schemas")):
        print("Relevant data has changed since the last commit, the api version needs to be incremented")
        assert current_version.follows(last_version)

import os
import json
import shutil

from utils.software_version import SoftwareVersion


def load_api_version(src_file: str) -> SoftwareVersion:
    try:
        with open(src_file, "r") as file_p:
            file_data = json.load(file_p)
            return SoftwareVersion.from_string(file_data["version"])
    except KeyError:
        return SoftwareVersion(0, 0, 1)


@pytest.mark.pr_only
def test_api_version_incrementation(temp_exists):
    current_version = load_api_version(os.path.join("api_docs", "api_specs.json"))
    print(current_version)
    source_dir = os.path.join(os.getcwd(), "temp", "repo", ".git")
    base_dir = os.path.join(os.getcwd(), ".git")
    print(f"Copying '{base_dir}' to '{source_dir}'")

    shutil.copytree(base_dir, source_dir)
    return_code = os.system("cd temp/repo && git reset --hard && git checkout origin/master")
    assert return_code == 0
    last_version = load_api_version(os.path.join("temp", "repo", "api_docs", "api_specs.json"))
    print(last_version)
    assert current_version.follows(last_version)

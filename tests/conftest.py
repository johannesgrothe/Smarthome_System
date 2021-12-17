import pytest

from exporters.script_params import PATH_TEMP_DIR
from exporters.temp_dir_manager import TempDirManager


@pytest.fixture
def temp_exists():
    print("Creating temp dir")
    TempDirManager(PATH_TEMP_DIR).assert_temp()
    yield None
    print("Removing temporary files")
    TempDirManager(PATH_TEMP_DIR).clean_temp()

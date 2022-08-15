import pytest

from exporters.def_params import PATH_TEMP_DIR
from utils.temp_dir_manager import TempDirManager


@pytest.fixture
def assert_temp() -> str:
    print("Creating temp dir")
    TempDirManager(PATH_TEMP_DIR).assert_temp()
    TempDirManager(PATH_TEMP_DIR).clean_temp()
    yield PATH_TEMP_DIR
    print("Removing temporary files")
    TempDirManager(PATH_TEMP_DIR).clean_temp()

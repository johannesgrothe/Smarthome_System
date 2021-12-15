import logging
import os


class TempDirManager:
    _path: str
    _logger: logging.Logger

    def __init__(self, path: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._path = path

    def assert_temp(self):
        if not os.path.isdir(self._path):
            os.mkdir(self._path)

    def clean_temp(self):
        for filename in [x for x
                         in os.listdir(self._path)
                         if os.path.isfile(os.path.join(self._path, x))]:
            self._logger.info(f"Deleting '{filename}'")
            os.remove(os.path.join(self._path, filename))

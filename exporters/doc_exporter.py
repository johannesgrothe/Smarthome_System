import logging
from abc import abstractmethod

from exporters.definitions_loader import DefinitionsLoader


class DocExporter:

    _logger: logging.Logger
    _definitions_file: str
    _definitions: dict

    def __init__(self, definitions: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._definitions_file = definitions
        self._definitions = DefinitionsLoader(self._definitions_file).get_definitions()
        self._logger.info("Definitions loaded successfully")

    @abstractmethod
    def export_docs(self, out_file: str):
        pass

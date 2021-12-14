"""Module for the definitions loader class"""
import os
import json
from jsonschema import validate, ValidationError
import logging


class DefinitionsLoader:
    """Loader class for the api definitions"""
    _definitions_file: str
    _definitions: dict
    _logger: logging.Logger

    def __init__(self, definitions: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._definitions_file = definitions
        try:
            self._load_definitions()
        except ValidationError as err:
            self._logger.error(err.args[0])
            raise Exception("Could not load api definition because of failed schema validation")

    def _load_definitions(self):
        with open(self._definitions_file, "r") as file_p:
            data = json.load(file_p)

        schema_path = os.path.abspath(os.path.join(self._definitions_file, os.pardir, data["$schema"]))

        with open(schema_path, "r") as file_p:
            schema = json.load(file_p)

        validate(data, schema)
        self._definitions = data

    def get_definitions(self) -> dict:
        """
        Returns the loaded and validated definitions

        :return: The loaded definitions
        """
        return self._definitions

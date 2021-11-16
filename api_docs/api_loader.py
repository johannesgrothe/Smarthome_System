"""Module for the api loader class"""
import os
import json
from jsonschema import validate, ValidationError
import logging


class ApiLoader:
    """Loader class for the api definitions"""
    _definitions_file: str
    _api_definition: dict
    _logger: logging.Logger

    def __init__(self, definitions: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._definitions_file = definitions
        try:
            self._load_api_definition()
        except ValidationError as err:
            self._logger.error(err.args[0])
            raise Exception("Could not load api definition because of failed schema validation")

    def _load_api_definition(self):
        with open(self._definitions_file, "r") as file_p:
            data = json.load(file_p)

        schema_path = os.path.abspath(os.path.join(self._definitions_file, os.pardir, data["$schema"]))

        with open(schema_path, "r") as file_p:
            schema = json.load(file_p)

        validate(data, schema)
        self._api_definition = data

    def get_definitions(self) -> dict:
        """
        Returns the loaded and validated api definitions

        :return: The loaded api definitions
        """
        return self._api_definition

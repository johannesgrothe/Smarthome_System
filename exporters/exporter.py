import logging
import os
from abc import abstractmethod, ABCMeta

from exporters.def_filenames import FILE_API_SPECS, FILE_GADGET_SPECS, FILE_HW_VARIANTS, FILE_SW_VARIANTS
from exporters.definitions_loader import DefinitionsLoader
from utils.schema_loader import SchemaLoader
from utils.software_version import SoftwareVersion

_api_specs_file = os.path.join("api_docs", "api_specs.json")
_gadget_specs_file = os.path.join("gadget_docs", "gadget_specs.json")
_schema_folder = "json_schemas"


class Exporter(metaclass=ABCMeta):
    _gadget_class_def: dict
    _gadgets_local: dict
    _gadgets_remote: dict

    _api_access_level_def: dict
    _api_endpoint_def: dict
    _api_version: SoftwareVersion
    _schema_data: dict

    _hw_variant_def: dict
    _sw_variant_def: dict

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

        gadget_def = DefinitionsLoader(FILE_GADGET_SPECS).get_definitions()
        self._gadget_class_def = gadget_def["gadget_classes"]
        self._gadgets_local = gadget_def["gadget_definitions"]["bridge_gadgets"]
        self._gadgets_remote = gadget_def["gadget_definitions"]["client_gadgets"]

        api_def = DefinitionsLoader(FILE_API_SPECS).get_definitions()
        self._api_endpoint_def = api_def["endpoints"]
        self._api_access_level_def = api_def["access_levels"]
        self._api_version = SoftwareVersion.from_string(api_def["version"])

        self._schema_data = SchemaLoader(_schema_folder).load_schemas()

        self._hw_variant_def = DefinitionsLoader(FILE_HW_VARIANTS).get_definitions()
        self._sw_variant_def = DefinitionsLoader(FILE_SW_VARIANTS).get_definitions()
        

    @abstractmethod
    def export(self, filename: str):
        pass

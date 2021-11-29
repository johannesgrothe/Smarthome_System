"""Module for the api constants exporter"""
import os.path
import sys
import logging

sys.path.append("..")

from api_loader import ApiLoader

# Path to the file containing the api definitions
_path_api_specs = os.path.join(os.getcwd(), "api_specs.json")

# Path to the json schemas referenced in the api specs file
_path_json_schemas = "json_schemas"

_export_file_docstring = "Collection of constants for all api uris"

_generated_header = [f"This file was generated by '{'/'.join(__file__.split('/')[-1:])}' at "
                     f"'https://github.com/johannesgrothe/Smarthome_System'",
                     f"Do not modify this file, modify '{'api_docs/api_specs.json'}' export.",
                     "Every change made will be overwritten at next export."]


class ApiConstantsExporter:
    """Class that handles the api doc exporting process"""

    _api_definition: dict

    def __init__(self, definitions: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._api_definition = ApiLoader(definitions).get_definitions()
        self._logger.info("Api definitions loaded successfully")

    def export_api_constants_python(self, out_file: str):
        lines = []

        lines.append(f"\"\"\"{_export_file_docstring}\"\"\"")
        lines.append("")

        for line in _generated_header:
            lines.append(f"# {line}")

        lines.append("")

        for mapping in self._api_definition["mappings"]:
            data = self._api_definition["mappings"][mapping]
            lines.append(f"# {data['title']}")
            lines.append(f"{data['uri']['var_name']} = \"{data['uri']['value']}\"")
            lines.append("")

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])

    def export_api_constants_cpp(self, out_file: str):
        lines = []

        lines.append(f"// {_export_file_docstring}")
        lines.append("")

        for line in _generated_header:
            lines.append(f"// {line}")

        lines.append("")

        for mapping in self._api_definition["mappings"]:
            data = self._api_definition["mappings"][mapping]
            lines.append(f"// {data['title']}")
            lines.append(f"#define {data['uri']['var_name']} \"{data['uri']['value']}\"")
            lines.append("")

        with open(out_file, "w") as file_p:
            file_p.writelines([x + "\n" for x in lines])


def main():
    exporter = ApiConstantsExporter(_path_api_specs)
    exporter.export_api_constants_python("../api_params.py")
    exporter.export_api_constants_cpp("../api_params.h")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()

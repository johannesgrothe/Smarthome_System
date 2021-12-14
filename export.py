import argparse
import logging

from exporters.script_params import *
from exporters.temp_dir_manager import TempDirManager
from exporters.api_constants_exporter import ApiConstantsExporter
from exporters.api_doc_exporter import ApiDocExporter


def export_api_constants():
    exporter = ApiConstantsExporter(PATH_API_SPECS)
    exporter.export_python(f"{PATH_FILE_API_CONSTANTS}.py")
    exporter.export_cpp(f"{PATH_FILE_API_CONSTANTS}.h")


def export_api_docs():
    exporter = ApiDocExporter(PATH_API_SPECS, PATH_JSON_SCHEMAS)
    exporter.export_api_doc(os.path.join(PATH_TEMP_DIR, NAME_FILE_API_DOCS))


def export_gadget_constants():
    # exporter = ApiConstantsExporter(PATH_API_SPECS)
    # exporter.export_python(f"{PATH_FILE_API_CONSTANTS}.py")
    # exporter.export_cpp(f"{PATH_FILE_API_CONSTANTS}.h")
    pass


def export_gadget_docs():
    # exporter = ApiDocExporter(PATH_API_SPECS, PATH_JSON_SCHEMAS)
    # exporter.export_api_doc(os.path.join(PATH_TEMP_DIR, NAME_FILE_API_DOCS))
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean_temp", action="store_true", default=False)
    parser.add_argument("--export_docs", action="store_true", default=False)
    parser.add_argument("--export_constants", action="store_true", default=False)
    return parser.parse_args()


def main():
    args = parse_args()

    if args.export_docs:
        TempDirManager(PATH_TEMP_DIR).assert_temp()
        if args.clean_temp:
            TempDirManager(PATH_TEMP_DIR).clean_temp()
        export_api_docs()
        export_gadget_docs()

    if args.export_constants:
        export_api_constants()
        export_gadget_constants()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()

import argparse
import logging
import sys

from exporters.gadget_doc_exporter import GadgetDocExporter
from exporters.script_params import *
from exporters.temp_dir_manager import TempDirManager
from exporters.api_constants_exporter import ApiConstantsExporter
from exporters.api_doc_exporter import ApiDocExporter
from exporters.gadget_constants_exporter import GadgetConstantsExporter
from system.exporters.gadget_api_doc_exporter import GadgetApiDocExporter


def export_api_constants():
    exporter = ApiConstantsExporter(PATH_API_SPECS)
    exporter.export_python(f"{PATH_FILE_API_CONSTANTS}.py")
    exporter.export_cpp(f"{PATH_FILE_API_CONSTANTS}.h")
    exporter.export_js(f"{PATH_FILE_API_CONSTANTS}.js")
    exporter.export_swift(f"{PATH_FILE_API_CONSTANTS}.swift")


def export_api_docs():
    exporter = ApiDocExporter(PATH_API_SPECS, PATH_JSON_SCHEMAS)
    exporter.export_docs(os.path.join(PATH_TEMP_DIR, NAME_FILE_API_DOCS))


def export_gadget_constants():
    exporter = GadgetConstantsExporter(PATH_GADGET_SPECS)
    exporter.export_python(f"{PATH_FILE_GADGET_CONSTANTS}.py")
    exporter.export_cpp(f"{PATH_FILE_GADGET_CONSTANTS}.h")
    exporter.export_js(f"{PATH_FILE_GADGET_CONSTANTS}.js")


def export_gadget_docs():
    exporter = GadgetDocExporter(PATH_GADGET_SPECS)
    exporter.export_docs(os.path.join(PATH_TEMP_DIR, NAME_FILE_GADGET_DOCS))

    exporter = GadgetApiDocExporter(PATH_GADGET_SPECS, PATH_JSON_SCHEMAS)
    exporter.export_docs(os.path.join(PATH_TEMP_DIR, NAME_FILE_GADGET_CLASS_DOCS))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean_temp", action="store_true", default=False)
    parser.add_argument("--export_docs", action="store_true", default=False)
    parser.add_argument("--export_constants", action="store_true", default=False)
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.export_docs and not args.export_constants:
        print("Congratz, ye did absolutely nothin', ye bawbag!")
        print("use -h for help on params")
        sys.exit(1)

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

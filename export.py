import argparse
import logging
import sys

from exporters.constants_exporter_gadgets_cpp import ConstantExporterGadgetsCpp
from exporters.constants_exporter_gadgets_js import ConstantExporterGadgetsJavaScript
from exporters.constants_exporter_gadgets_python import ConstantExporterGadgetsPython
from exporters.constants_exporter_gadgets_swift import ConstantExporterGadgetsSwift
from utils.temp_dir_manager import TempDirManager
from exporters.constants_exporter_api_cpp import ConstantExporterApiCpp
from exporters.constants_exporter_api_js import ConstantExporterApiJavaScript
from exporters.constants_exporter_api_python import ConstantExporterApiPython
from exporters.constants_exporter_api_swift import ConstantExporterApiSwift
from exporters.def_filenames import *
from exporters.def_params import PATH_TEMP_DIR
from exporters.wiki_export_gadget_classes import WikiExporterGadgetClasses
from exporters.wiki_export_gadgets_local import WikiExporterGadgetsLocal
from exporters.wiki_export_gadgets_remote import WikiExporterGadgetsRemote
from exporters.wiki_exporter_api_access_levels import WikiExporterApiAccessLevels
from exporters.wiki_exporter_api_endpoints_bridge import WikiExporterApiEndpointsBridge
from exporters.wiki_exporter_api_endpoints_client import WikiExporterApiEndpointsClient


def export_constants():
    ConstantExporterApiPython().export(FILE_API_CONSTANTS_PY)
    ConstantExporterApiJavaScript().export(FILE_API_CONSTANTS_JS)
    ConstantExporterApiCpp().export(FILE_API_CONSTANTS_CPP)
    ConstantExporterApiSwift().export(FILE_API_CONSTANTS_SWIFT)

    ConstantExporterGadgetsPython().export(FILE_GADGET_CONSTANTS_PY)
    ConstantExporterGadgetsCpp().export(FILE_GADGET_CONSTANTS_CPP)
    ConstantExporterGadgetsJavaScript().export(FILE_GADGET_CONSTANTS_JS)
    ConstantExporterGadgetsSwift().export(FILE_GADGET_CONSTANTS_SWIFT)


def export_wiki():
    WikiExporterApiAccessLevels().export(os.path.join(PATH_TEMP_DIR, FILE_API_ACCESS_LEVELS))
    WikiExporterApiEndpointsBridge().export(os.path.join(PATH_TEMP_DIR, FILE_API_BRIDGE))
    WikiExporterApiEndpointsClient().export(os.path.join(PATH_TEMP_DIR, FILE_API_CLIENT))

    WikiExporterGadgetClasses().export(os.path.join(PATH_TEMP_DIR, FILE_GADGET_CLASSES))
    WikiExporterGadgetsLocal().export(os.path.join(PATH_TEMP_DIR, FILE_GADGETS_BRIDGE))
    WikiExporterGadgetsRemote().export(os.path.join(PATH_TEMP_DIR, FILE_GADGETS_CLIENT))


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
        export_wiki()

    if args.export_constants:
        export_constants()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()

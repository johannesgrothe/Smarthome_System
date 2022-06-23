import argparse
import logging
import sys

from system.utils.temp_dir_manager import TempDirManager
from system.exporters.constants_exporter_api_cpp import ConstantExporterApiCpp
from system.exporters.constants_exporter_api_js import ConstantExporterApiJavaScript
from system.exporters.constants_exporter_api_python import ConstantExporterApiPython
from system.exporters.constants_exporter_api_swift import ConstantExporterApiSwift
from system.exporters.def_filenames import *
from system.exporters.def_params import PATH_TEMP_DIR
from system.exporters.wiki_export_gadget_classes import WikiExporterGadgetClasses
from system.exporters.wiki_export_gadgets_local import WikiExporterGadgetsLocal
from system.exporters.wiki_export_gadgets_remote import WikiExporterGadgetsRemote
from system.exporters.wiki_exporter_api_access_levels import WikiExporterApiAccessLevels
from system.exporters.wiki_exporter_api_endpoints_bridge import WikiExporterApiEndpointsBridge
from system.exporters.wiki_exporter_api_endpoints_client import WikiExporterApiEndpointsClient


# def export_api_constants():
#     exporter = ApiConstantsExporter(PATH_API_SPECS)
#     exporter.export_python(FILE_API_CONSTANTS_PY)
#     exporter.export_cpp(FILE_API_CONSTANTS_CPP)
#     exporter.export_js(FILE_API_CONSTANTS_JS)
#     exporter.export_swift(FILE_API_CONSTANTS_SWIFT)


def export_constants():
    ConstantExporterApiPython().export(FILE_API_CONSTANTS_PY)
    ConstantExporterApiJavaScript().export(FILE_API_CONSTANTS_JS)
    ConstantExporterApiCpp().export(FILE_API_CONSTANTS_CPP)
    ConstantExporterApiSwift().export(FILE_API_CONSTANTS_SWIFT)


def export_wiki():
    WikiExporterApiAccessLevels().export(os.path.join(PATH_TEMP_DIR, FILE_API_ACCESS_LEVELS))
    WikiExporterApiEndpointsBridge().export(os.path.join(PATH_TEMP_DIR, FILE_API_BRIDGE))
    WikiExporterApiEndpointsClient().export(os.path.join(PATH_TEMP_DIR, FILE_API_CLIENT))

    WikiExporterGadgetClasses().export(os.path.join(PATH_TEMP_DIR, FILE_GADGET_CLASSES))
    WikiExporterGadgetsLocal().export(os.path.join(PATH_TEMP_DIR, FILE_GADGETS_BRIDGE))
    WikiExporterGadgetsRemote().export(os.path.join(PATH_TEMP_DIR, FILE_GADGETS_CLIENT))


# def export_gadget_constants():
#     exporter = GadgetConstantsExporter(PATH_GADGET_SPECS)
#     exporter.export_python(f"{PATH_FILE_GADGET_CONSTANTS}.py")
#     exporter.export_cpp(f"{PATH_FILE_GADGET_CONSTANTS}.h")
#     exporter.export_js(f"{PATH_FILE_GADGET_CONSTANTS}.js")


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

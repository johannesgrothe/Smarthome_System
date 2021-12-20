from exporters.doc_exporter import DocExporter
from exporters.script_params import PATH_FILE_GADGET_CONSTANTS
from utils.markdown_file import *


class GadgetDocExporter(DocExporter):
    """Class that handles the gadget doc exporting process"""

    def __init__(self, definitions: str):
        super().__init__(definitions)

    @staticmethod
    def _gen_enum_table(data: dict) -> MarkdownTable:
        overview = {}
        for key, data in data["items"].items():
            val = data["enum_value"]
            if val in overview:
                raise Exception(f"Double Identifier: {val}")
            overview[val] = key
        key_list = [x for x in overview.keys()]
        key_list.sort()

        status_table = MarkdownTable(["Int Identifier", "String Identifier"])
        for key in key_list:
            status_table.add_line([str(key), overview[key]])
        return status_table

    @staticmethod
    def _add_characteristic_info(key: str, data: dict, file: MarkdownFile):
        file.add(MarkdownHeader(data["name"], 2))
        file.add(MarkdownText(data["description"]))

        identifier_table = MarkdownTable(["Parameter Name", "Parameter Value"])
        identifier_table.add_line(["Int Identifier", str(data['enum_value'])])
        identifier_table.add_line(["String Identifier", key])
        file.add(identifier_table)

    @staticmethod
    def _add_gadget_info(key: str, data: dict, file: MarkdownFile):
        file.add(MarkdownHeader(data["name"], 2))
        file.add(MarkdownText(data["description"]))

        identifier_table = MarkdownTable(["Parameter Name", "Parameter Value"])
        identifier_table.add_line(["Int Identifier", str(data['enum_value'])])
        identifier_table.add_line(["String Identifier", key])
        identifier_table.add_line(["IR Required", str(data['ir_required'])])
        identifier_table.add_line(["Radio Required", str(data['radio_required'])])
        file.add(identifier_table)

    def export_docs(self, out_file: str):
        file = MarkdownFile()
        file.add(MarkdownHeader(self._definitions["title"], 0))
        file.add(MarkdownText(self._definitions["description"]))

        file.add(MarkdownDivider())
        self._add_exported_libraries(PATH_FILE_GADGET_CONSTANTS, file)
        file.add(MarkdownDivider())

        characteristics_data = self._definitions["characteristic_definitions"]
        file.add(MarkdownHeader(characteristics_data["title"], 1))
        file.add(MarkdownText(characteristics_data["description"]))

        file.add(self._gen_enum_table(characteristics_data))

        for key, data in characteristics_data["items"].items():
            self._add_characteristic_info(key, data, file)

            file.add(MarkdownDivider())

        for _, gadget_platform in self._definitions["gadget_definitions"].items():
            file.add(MarkdownHeader(gadget_platform["title"], 1))
            file.add(MarkdownText(gadget_platform["description"]))

            if not gadget_platform["items"]:
                file.add(MarkdownText("This platform has no gadgets specified yet."))
                file.add(MarkdownDivider())
            else:
                file.add(self._gen_enum_table(gadget_platform))

                for g_key, gadget_data in gadget_platform["items"].items():
                    self._add_gadget_info(g_key, gadget_data, file)

                    file.add(MarkdownHeader("Characteristics", 3))
                    if gadget_data["characteristics"]:
                        characteristics_list = MarkdownList()
                        for c_identifier in gadget_data["characteristics"]:
                            c_data = self._definitions["characteristic_definitions"]["items"][c_identifier]
                            characteristics_list.add_line(f"{c_data['name']}")
                        file.add(characteristics_list)
                    else:
                        file.add(MarkdownText("This gadget does not have any characteristics attached"))

                    file.add(MarkdownHeader("Ports", 3))


                    file.add(MarkdownHeader("Config", 3))

                    file.add(MarkdownDivider())

        file.save(out_file)

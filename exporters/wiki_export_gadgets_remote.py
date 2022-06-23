import json

from system.exporters.wiki_export import WikiExporterGadgets
from system.utils.markdown_file import *


class WikiExporterGadgetsRemote(WikiExporterGadgets):
    def export(self, filename: str):
        file = MarkdownFile()
        file.add(MarkdownHeader(self._gadgets_remote["title"], 0))
        file.add(MarkdownText(self._gadgets_remote["description"]))

        file.add(self._gen_enum_table(self._gadgets_remote["items"]))

        for g_key, gadget_data in self._gadgets_remote["items"].items():
            file.add(MarkdownHeader(gadget_data["name"], 1))
            file.add(MarkdownText(gadget_data["description"]))

            identifier_table = MarkdownTable(["Parameter Name", "Parameter Value"])
            identifier_table.add_line(["Int Identifier", str(gadget_data['enum_value'])])
            identifier_table.add_line(["String Identifier", g_key])
            identifier_table.add_line(["IR Required", str(gadget_data['ir_required'])])
            identifier_table.add_line(["Radio Required", str(gadget_data['radio_required'])])
            file.add(identifier_table)

            if "ports" in gadget_data:
                file.add(MarkdownHeader("Ports", 2))
                if gadget_data["ports"]:
                    characteristics_list = MarkdownList()
                    for port, data in gadget_data["ports"].items():
                        characteristics_list.add_line(f"{port}: {data['description']}")
                    file.add(characteristics_list)
                else:
                    file.add(MarkdownText("This gadget does not require any hardware port access"))

            file.add(MarkdownHeader("Config", 2))
            if gadget_data["config"]:
                file.add(MarkdownCode(json.dumps(gadget_data['config'],
                                                 sort_keys=True,
                                                 indent=2,
                                                 separators=(',', ': ')),
                                      block=True,
                                      language="json"))
            else:
                file.add(MarkdownText("This gadget does not require any additional configuration json"))

            file.add(MarkdownDivider())

        file.save(filename)

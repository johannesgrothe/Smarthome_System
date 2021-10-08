from requirements_manager import RequirementsManager
from requirements_exporter import RequirementsExporter
from tools.cli_helpers import ask_for_continue, select_option

import argparse


class RequirementsManagerCLI:

    @classmethod
    def _print_requirement(cls, req_data: dict):
        status_str = "Valid" if req_data['status'] else "Deprecated"
        print(req_data['title'])
        print(f"ID: {req_data['id']}       Owner: {req_data['owner']}       Status: {status_str}")
        print(f"Description: {req_data['description']}")
        for story in req_data['userstories']:
            print(f"  - {story}")

    @classmethod
    def _print_requirements(cls, req_data: list):
        print("List of all selected requirements:")
        for req in req_data:
            cls._print_requirement(req)
            print()

    @classmethod
    def _add_requirement(cls, manager: RequirementsManager):
        req = {"title": None,
               "owner": None,
               "description": None,
               "userstories": []}
        changed = False
        while True:
            print(f"Title: {req['title']}")
            print(f"Owner: {req['owner']}")
            print(f"Description: {req['description']}")
            print(f"Userstories [{len(req['userstories'])}]")
            for story in req['userstories']:
                print(f"  - {story}")
            print()

            back_option = "Back"
            if changed:
                back_option = "Discard and Exit"

            task = select_option(["Edit Title",
                                  "Edit Description",
                                  "Edit Owner",
                                  "Add Userstory",
                                  "Reset Userstories",
                                  "Save and Exit"],
                                 "task",
                                 back_option)
            if task == -1:
                if changed and not ask_for_continue("Do you want to quit?"):
                    continue
                break

            if task == 5:
                manager.add_requirement(req["title"],
                                        req["description"],
                                        req["userstories"],
                                        req["owner"])
                break

            if task == 0:
                changed = True
                entered_value = input("Please enter the title:\n")
                if not entered_value:
                    entered_value = None
                req["title"] = entered_value

            if task == 1:
                changed = True
                entered_value = input("Please enter the description:\n")
                if not entered_value:
                    entered_value = None
                req["description"] = entered_value

            if task == 2:
                changed = True
                entered_value = input("Please enter the owner:\n")
                if not entered_value:
                    entered_value = None
                req["owner"] = entered_value

            if task == 3:
                changed = True
                entered_value = input("Please enter the userstory:\n")
                if not entered_value:
                    entered_value = None
                req["userstories"].append(entered_value)

            if task == 4:
                if ask_for_continue("Do you want to reset the userstories?"):
                    req["userstories"] = []

    @classmethod
    def _export_requirements(cls, manager: RequirementsManager):
        requirements = manager.get_requirements(None)
        RequirementsExporter.export_markdown(requirements, "requirements.md")

    @classmethod
    def _view_requirements(cls, manager: RequirementsManager):
        all_reqs = manager.get_requirements(None)
        valid_reqs = manager.get_requirements(True)
        invalid_reqs = manager.get_requirements(False)

        option = select_option([f"All ({len(all_reqs)})",
                                f"Valid only ({len(valid_reqs)})",
                                f"Invalid only ({len(invalid_reqs)})"],
                               "which requirements to view",
                               "Back")

        if option == -1:
            return
        elif option == 0:
            cls._print_requirements(all_reqs)
        elif option == 1:
            cls._print_requirements(valid_reqs)
        elif option == 2:
            cls._print_requirements(invalid_reqs)
        # print()
        # print()

    @classmethod
    def run(cls):
        print("Starting CLI...")
        manager = RequirementsManager()
        while True:
            option = select_option(["View Requirements", "Export Requirements", "Add Requirement"],
                                   "option",
                                   "Exit")
            if option == -1:
                break
            elif option == 0:
                cls._view_requirements(manager)
            elif option == 1:
                cls._export_requirements(manager)
            elif option == 2:
                cls._add_requirement(manager)
        print("Saving and quitting...")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Smarthome requirement management tool')
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace):
    RequirementsManagerCLI.run()


if __name__ == "__main__":
    script_args = parse_args()
    main(script_args)

from requirements_manager import RequirementsManager
from requirements_exporter import RequirementsExporter
from tools.cli_helpers import ask_for_continue, select_option

import argparse


class RequirementsManagerCLI:

    @classmethod
    def _print_requirement(cls, req_data: dict):
        print(f"ID: {req_data['id']}")

    @classmethod
    def _print_requirements(cls, req_data: list):
        print("List of all selected requirements:")
        for req in req_data:
            cls._print_requirement(req)
            print()

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
        print()
        print()

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

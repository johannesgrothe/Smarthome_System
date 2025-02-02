import json
from pathlib import Path

from utils.cpp_file import CppFile, CppEnumClass


def export_cpp(hw_data: dict, sw_data: dict, target: Path) -> None:
    file = CppFile()
    hw_variants_enum = CppEnumClass("HwVariant",
                                    hw_data["description"])

    hw_variants_enum.add_element("unknown", 0, "Element representing any error case")

    for i, variant_data in enumerate(hw_data["variants"]):
        hw_variants_enum.add_element(variant_data, i + 1, variant_data["description"])

    file.add(hw_variants_enum)

    sw_variants_enum = CppEnumClass("SwVariant",
                                    sw_data["description"])

    sw_variants_enum.add_element("unknown", 0, "Element representing any error case")

    for i, variant_data in enumerate(sw_data["variants"]):
        sw_variants_enum.add_element(variant_data, i + 1, variant_data["description"])

    file.add(sw_variants_enum)

    file.save(target.as_posix())


def export_python(hw_data: dict, sw_data: dict, target: Path) -> None:
    pass


def load_json(path: Path) -> dict:
    with open(path, "r") as file_p:
        return json.load(file_p)


def main():
    target_dir = Path(__file__).parent.parent
    file_dir = Path(__file__).parent

    hw_data = load_json(file_dir / "hw_variants.json")
    sw_data = load_json(file_dir / "sw_variants.json")

    export_cpp(hw_data, sw_data, target_dir / "variants.cpp")
    export_python(hw_data, sw_data, target_dir / "variants.py")


if __name__ == "__main__":
    main()

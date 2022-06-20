"""Module for the json schema formatter class"""
import json
from typing import Union, Tuple


class JsonSchemaFormatter:
    """Class to provide a json schema formatter functionality"""

    @classmethod
    def _is_optional(cls, type_data) -> bool:
        if not isinstance(type_data, list):
            return False
        return "null" in type_data

    @classmethod
    def _extract_type(cls, type_data) -> str:
        if isinstance(type_data, str):
            return type_data

        elif isinstance(type_data, list):
            if "null" in type_data:
                type_data.remove("null")

            if len(type_data) == 1:
                return type_data[0]
            else:
                buf_str = ""
                for elem in type_data:
                    buf_str += elem + ", "
                buf_str.strip().strip(",")
                return buf_str

    @staticmethod
    def _stringify_json(data: Union[list, dict]) -> str:
        return json.dumps(data, indent=2, sort_keys=True)

    @classmethod
    def _encode(cls, key: str, in_schema: dict) -> Tuple[str, Union[str, list, dict]]:
        out_key = key
        if "type" not in in_schema:
            return out_key, "<err>"

        is_optional = cls._is_optional(in_schema["type"])
        if is_optional:
            out_key = "[" + out_key + "]"

        s_type = cls._extract_type(in_schema["type"])

        if s_type == "string":
            return out_key, "<string>"
        elif s_type == "boolean":
            return out_key, "<boolean>"
        elif s_type == "integer":
            if "minimum" in in_schema and in_schema["minimum"] >= 0:
                return out_key, "<uint>"
            return out_key, "<int>"
        elif s_type == "array":
            _, data = cls._encode(key, in_schema["items"]) if "items" in in_schema else "<???>"
            return out_key, [data]
        elif s_type == "object" or s_type == "Optional<object>":
            buf_data = {}

            if "properties" in in_schema and in_schema["properties"]:
                for prop, prop_data in in_schema["properties"].items():
                    prop, data = cls._encode(prop, prop_data)
                    buf_data[prop] = data

            if "additionalProperties" in in_schema and in_schema["additionalProperties"]:
                prop, data = cls._encode("<any>", in_schema["additionalProperties"])
                buf_data[prop] = data

            if "patternProperties" in in_schema and in_schema["patternProperties"]:
                for prop, prop_data in in_schema["patternProperties"].items():
                    prop, data = cls._encode(f"<{prop}>", prop_data)
                    buf_data[prop] = data
                    # buf_data[f"<{prop}>"] = cls._encode(in_schema["patternProperties"][prop])
            return out_key, buf_data
        elif s_type.startswith("Optional"):
            if "integer" in s_type:
                if "minimum" in in_schema and in_schema["minimum"] >= 0:
                    s_type = s_type.replace("integer", "uint")
                else:
                    s_type = s_type.replace("integer", "int")
            return out_key, s_type
        else:
            return out_key, "<???>"

    @classmethod
    def shorten_schema(cls, in_schema: dict) -> str:
        _, data = cls._encode("", in_schema)
        return cls._stringify_json(data)

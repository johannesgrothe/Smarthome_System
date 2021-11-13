"""Module for the json schema formatter class"""
import json
from typing import Union


class JsonSchemaFormatter:
    """Class to provide a json schema formatter functionality"""

    @classmethod
    def _extract_type(cls, type_data) -> str:
        if isinstance(type_data, str):
            return type_data

        elif isinstance(type_data, list):
            if len(type_data) == 1:
                return type_data[0]
            elif "null" in type_data:
                buf_data = type_data.copy()
                buf_data.remove("null")
                return f"Optional<{cls._extract_type(buf_data)}>"
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
    def _encode(cls, in_schema: dict) -> Union[str, list, dict]:
        if "type" not in in_schema:
            return "<err>"

        s_type = cls._extract_type(in_schema["type"])

        if s_type == "string":
            return "<string>"
        elif s_type == "boolean":
            return "<boolean>"
        elif s_type.startswith("Optional"):
            if "integer" in s_type:
                if "minimum" in in_schema and in_schema["minimum"] >= 0:
                    s_type = s_type.replace("integer", "uint")
                else:
                    s_type = s_type.replace("integer", "int")
            return s_type
        elif s_type == "integer":
            if "minimum" in in_schema and in_schema["minimum"] >= 0:
                return "<uint>"
            return "<int>"
        elif s_type == "array":
            data = cls._encode(in_schema["items"]) if "items" in in_schema else "<???>"
            return [data]
        elif s_type == "object":
            buf_data = {}
            if "properties" in in_schema:
                for prop in in_schema["properties"]:
                    buf_data[prop] = cls._encode(in_schema["properties"][prop])
            return buf_data
        else:
            return "<???>"

    @classmethod
    def shorten_schema(cls, in_schema: dict) -> str:
        return cls._stringify_json(cls._encode(in_schema))

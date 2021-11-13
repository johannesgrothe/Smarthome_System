"""Module for the schema loader"""
import json
import os


class SchemaLoader:
    """Schema loader class"""

    _schema_folder: str

    def __init__(self, schema_folder: str):
        self._schema_folder = schema_folder

    @classmethod
    def _fix_schema(cls, schema: dict, schema_list: dict) -> dict:
        buf_schema = schema.copy()
        for key in buf_schema:
            if key == "$ref":
                try:
                    schema_name = buf_schema[key][:-5]
                    return schema_list[schema_name]
                except KeyError:
                    return buf_schema
            elif isinstance(buf_schema[key], dict):
                buf_schema[key] = cls._fix_schema(buf_schema[key], schema_list)
        return buf_schema

    def load_schemas(self) -> dict:
        """
        Reloads all the schema data from the disk and resolves the references

        :return: None
        """
        buf_schemas = {}
        relevant_files = [file for file in os.listdir(self._schema_folder)
                          if os.path.isfile(os.path.join(self._schema_folder, file))
                          and file.endswith('.json')]
        for filename in relevant_files:
            with open(os.path.join(self._schema_folder, filename)) as f:
                data = json.load(f)
                try:
                    del data["$schema"]
                except KeyError:
                    pass
                buf_schemas[filename[:-5]] = data

        fixed_schemas = True
        runs = 0
        while fixed_schemas and runs <= 15:
            runs += 1
            fixed_schemas = 0
            for schema_name in buf_schemas:
                old_schema = buf_schemas[schema_name]
                new_schema = self._fix_schema(old_schema, buf_schemas)
                if new_schema != old_schema:
                    buf_schemas[schema_name] = new_schema
                    fixed_schemas = True

        return buf_schemas
